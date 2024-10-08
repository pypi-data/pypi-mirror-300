import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


class FileStorage:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def make_path(self, cls, name, prefix):
        path = cls.__name__.lower()
        if prefix:
            path = Path(self.root, prefix, path, name)
        else:
            path = Path(self.root, path, name)
        return path

    async def save_file(self, name, src):
        path = Path(self.root, "file", name)
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        with tmp.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        tmp.rename(path)

    async def save(self, name, data, prefix=""):
        path = self.make_path(type(data), name, prefix)
        await self.save_into(data, path)

    async def save_into(self, data, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(data.model_dump_json(indent=2))
        tmp.rename(path)

    async def load(self, cls, name, prefix=""):
        path = self.make_path(cls, name, prefix)
        return await self.load_from(cls, path)

    async def load_from(self, cls, path):
        try:
            text = path.read_text()
        except FileNotFoundError:
            return None
        return cls.model_validate_json(text)

    async def save_pending(self, what, data):
        now = datetime.now(UTC).isoformat(sep="T", timespec="seconds")
        now = now.replace("+00:00", "Z")
        path = Path(self.root, "pending", what, f"{now}+{uuid4().hex}.json")
        tmp = path.with_suffix(".tmp")
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(data, indent=2))
        tmp.rename(path)

    async def find_pending(self, what):
        files = Path(self.root, "pending", what).glob("*.json")

        class Pending:
            def __init__(self, file):
                self.f = file

            async def done(self):
                self.f.unlink()

        for file in sorted(files):
            yield Pending(file), json.loads(file.read_text())
