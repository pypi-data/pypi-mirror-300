import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


class FileStorage:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def dump(self):
        for f in sorted(self.root.glob("**/*")):
            print(f)
            if not f.is_dir():
                print(f.read_text())

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
        subdir = f"{prefix}{type(data).__name__.lower()}"
        path = Path(self.root, subdir, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(data.model_dump_json(indent=2))
        tmp.rename(path)

    async def load(self, cls, name, prefix=""):
        try:
            subdir = f"{prefix}{cls.__name__.lower()}"
            path = Path(self.root, subdir, name)
            text = path.read_text()
        except FileNotFoundError:
            return None
        return cls.model_validate_json(text)

    async def save_pending(self, what, data):
        when = (
            datetime.now(UTC)
            .isoformat(sep="T", timespec="seconds")
            .replace("+00:00", "Z")
        )
        path = Path(self.root, "pending", what, f"{when}+{uuid4().hex}.json")
        tmp = path.with_suffix(".tmp")
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(data, indent=2))
        tmp.rename(path)

    async def find_pending(self, what):
        files = Path(self.root, "pending", what).glob("*.json")

        class Pending:
            def __init__(self, file):
                self.f = file

            def done(self):
                self.f.unlink()

        for file in sorted(files):
            yield Pending(file), json.loads(file.read_text())
