from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dpkit.api import Details, Module, User
from dpkit.api.app import make_app
from dpkit.api.store import Store

auth = {"Authorization": "Bearer 123"}


@pytest.fixture
def client(tmp_path: Path):
    modules = {
        "fg": Module(
            id="fg",
            inputs={
                "wsi": Details(types=["application/dicom"]),
            },
        ),
    }

    users = {
        "123": User(
            id="bob@example.com",
            organization="acme",
        ),
    }

    return TestClient(make_app(Store(root=tmp_path), modules, users))


def test_app_v1_should_404(client):
    r = client.get("/v1")
    assert r.status_code == 404


def test_app_v1_fileset_should_405(client):
    r = client.get("/v1/fileset")
    assert r.status_code == 405


def test_app_v1_fileset_should_403_without_authorization(client):
    r = client.get("/v1/fileset/123")
    assert r.status_code == 403


def test_app_v1_fileset_should_422_without_body(client):
    r = client.post("/v1/fileset", headers=auth)
    assert r.status_code == 422


def test_app_v1_fileset_should_400_with_empty_inputs(client):
    data = {"files": []}
    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 400


def test_app_v1_fileset_should_400_with_invalid_path(client):
    data = {
        "files": [
            {
                "path": "../coco.json",
                "size": 32,
                "sha1": "da6b71f1ef8365676c385d40dd55f38aa5c726da",
            }
        ]
    }

    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 400


def test_app_v1_fileset_should_400_with_duplicates(client):
    data = {
        "files": [
            {
                "path": "coco.json",
                "size": 32,
                "sha1": "da6b71f1ef8365676c385d40dd55f38aa5c726da",
            },
            {
                "path": "coco.json",
                "size": 16,
                "sha1": "ad627c5aa83f55dd04d583c6765638fe1f17b6ad",
            },
        ]
    }

    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 400


def test_app_v1_fileset_should_200(client):
    data = {
        "files": [
            {
                "path": "a.json",
                "size": 32,
                "sha1": "da6b71f1ef8365676c385d40dd55f38aa5c726da",
            },
            {
                "path": "b.json",
                "size": 16,
                "sha1": "ad627c5aa83f55dd04d583c6765638fe1f17b6ad",
            },
        ]
    }

    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 200
    assert r.json().get("id") == "9eb5f779c814c70a9128c90d9d778d788546e877"


def test_app_v1_fileset_should_200_when_pending_and_400_after(client):
    id = "12953cb764b0892ac94e7b3cdff6fefbe2d1ea8f"
    data = {
        "files": [
            {
                "path": "a.json",
                "size": 32,
                "sha1": "da6b71f1ef8365676c385d40dd55f38aa5c726da",
            },
        ]
    }

    # creation
    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 200
    a = r.json()
    assert a["id"] == id
    assert a["state"] == "pending"
    assert a["metadata"] is None
    assert len(a["changes"]) == 1

    data["metadata"] = {"hello": "world"}

    # update is OK
    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 200
    b = r.json()
    assert b.get("id") == id
    assert b["state"] == "pending"
    assert b["created"] == a["created"]
    assert b["files"] == a["files"]
    assert b["metadata"] == {"hello": "world"}
    assert len(b["changes"]) == 2

    # get is OK
    r = client.get(f"/v1/fileset/{id}", headers=auth)
    assert r.status_code == 200

    # mark as complete
    r = client.post(f"/v1/fileset/{id}", headers=auth)
    assert r.status_code == 200

    # get is OK
    r = client.get(f"/v1/fileset/{id}", headers=auth)
    assert r.status_code == 200
    c = r.json()
    assert c["state"] == "completing"
    assert len(c["changes"]) == 3

    # update fails
    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 400


def test_app_v1_module_list_should_200(client):
    r = client.get("/v1/module", headers=auth)
    assert r.status_code == 200
    assert r.json() == ["fg"]


def test_app_v1_module_get_should_404_with_unknown(client):
    r = client.get("/v1/module/bla", headers=auth)
    assert r.status_code == 404


def test_app_v1_module_get_should_200(client):
    r = client.get("/v1/module/fg", headers=auth)
    assert r.status_code == 200
    m = Module.model_validate_json(r.text)
    assert m.id == "fg"


def test_app_v1_analysis_post_should_422_with_no_body(client):
    r = client.post("/v1/analysis", headers=auth)
    assert r.status_code == 422


def test_app_v1_analysis_post_should_422_with_no_inputs(client):
    data = {
        "module": "arg",
    }

    r = client.post("/v1/analysis", json=data, headers=auth)
    assert r.status_code == 422


def test_app_v1_analysis_post_should_422_with_no_module(client):
    data = {
        "inputs": {},
    }

    r = client.post("/v1/analysis", json=data, headers=auth)
    assert r.status_code == 422


def test_app_v1_analysis_post_should_400_with_unknown_module(client):
    data = {
        "module": "arg",
        "inputs": {},
    }

    r = client.post("/v1/analysis", json=data, headers=auth)
    assert r.status_code == 400


def test_app_v1_analysis_post_should_400_with_missing_input(client):
    data = {
        "module": "fg",
        "inputs": {},
    }

    r = client.post("/v1/analysis", json=data, headers=auth)
    assert r.status_code == 400


def test_app_v1_analysis_post_should_400_with_unknown_fileset(client):
    data = {
        "module": "fg",
        "inputs": {
            "wsi": "@asdf",
        },
    }

    r = client.post("/v1/analysis", json=data, headers=auth)
    assert r.status_code == 400


def test_app_v1_analysis_post_should_200(client):
    data = {
        "files": [
            {
                "path": "a.json",
                "size": 32,
                "sha1": "da6b71f1ef8365676c385d40dd55f38aa5c726da",
            },
        ]
    }

    r = client.post("/v1/fileset", json=data, headers=auth)
    assert r.status_code == 200
    fileset = r.json()

    data = {
        "module": "fg",
        "inputs": {
            "wsi": "@" + fileset["id"],
        },
    }

    r = client.post("/v1/analysis", json=data, headers=auth)
    assert r.status_code == 200

    id = "32814b74735f58fd5fd3388c3968405670b6d791"
    analysis = r.json()
    assert analysis["id"] == id

    r = client.get(f"/v1/analysis/{id}", headers=auth)
    assert r.status_code == 200
    assert r.json() == analysis
