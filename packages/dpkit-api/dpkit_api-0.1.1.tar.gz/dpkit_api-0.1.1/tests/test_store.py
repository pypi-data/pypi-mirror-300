from pathlib import Path

from dpkit.api import Details, Module, User
from dpkit.api.store import Store


async def test_store(tmp_path: Path) -> None:
    bob = User(
        id="bob",
        organization="acme",
    )

    store = Store(storage="file", root=Path(tmp_path, "db"))

    # test files
    a = Path(tmp_path, "a")
    b = Path(tmp_path, "b")
    a.write_text("123")
    b.write_text("abc")

    # write test files
    files = await store.save_files([a, b], root=tmp_path)

    # test fileset
    fs = await store.make_fileset(
        user=bob,
        files=files,
        mime="auto",
        metadata={
            "foo": "123",
            "bar": {
                "hello": "world",
            },
        },
    )

    # test module
    module = Module(
        id="patate",
        inputs={
            "ref": Details(
                types=["any"],
            ),
            "tag": Details(
                types=["any"],
            ),
        },
    )

    # request analysis
    analysis = await store.make_analysis(
        user=bob,
        module=module,
        inputs=dict(
            ref=f"@{fs.id}",
            tag=f"@{fs.id}/bar/hello",
        ),
    )

    done = []
    async for item, pending in store.pending("analysis"):
        done.append(pending)
        assert pending == analysis.id
        item.done()

    # make sure ID is deterministic
    assert done == ["6441f25d320312ca30efec553b7197e6327165fa"]
