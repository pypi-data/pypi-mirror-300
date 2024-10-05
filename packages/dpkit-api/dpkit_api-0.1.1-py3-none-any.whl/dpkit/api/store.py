import json
from collections import Counter
from datetime import UTC, datetime
from hashlib import file_digest, sha1
from pathlib import Path

from dpkit.api import Analysis, File, FileSet


class Store:
    def __init__(self, storage: str = "file", **kwargs):
        if storage == "file":
            from dpkit.api.storage.file import FileStorage

            self.storage = FileStorage(**kwargs)
            return

        raise RuntimeError(f"unknown storage driver {storage}")

    def make_fileset_name(self, user, files):
        fileset = {
            "owner": user.organization,
            "files": [],
        }

        for file in sorted(files, key=lambda f: f.path):
            fileset["files"].append(
                {
                    "path": file.path,
                    "sha1": file.sha1,
                    "size": file.size,
                }
            )

        return sha1(json.dumps(fileset, sort_keys=True).encode()).hexdigest()

    def make_analysis_name(self, user, module, inputs):
        analysis = {
            "owner": user.organization,
            "module": module,
            "inputs": inputs,
        }

        return sha1(json.dumps(analysis, sort_keys=True).encode()).hexdigest()

    async def save_files(self, paths, root):
        files = []
        for path in paths:
            with path.open("rb") as fd:
                name = file_digest(fd, "sha1").hexdigest()
                data = File(
                    path=str(path.resolve().relative_to(root)),
                    sha1=name,
                    size=path.stat().st_size,
                )

                files.append(data)
                await self.storage.save_file(name, fd)

        return files

    async def make_fileset(self, user, files, mime, metadata):
        now = datetime.now(UTC).replace(microsecond=0)

        # no files?
        paths = [Path(f.path) for f in files]
        if len(files) == 0:
            raise RuntimeError("expecting files")

        # perform some validation on file path
        for path in paths:
            if len(path.parts) == 0 or path.parts[0] == "/" or ".." in path.parts:
                raise RuntimeError(f"invalid path: {str(path)}")

        # check for duplicates
        duplicates = [str(path) for path, count in Counter(paths).items() if count > 1]
        if len(duplicates) != 0:
            raise RuntimeError(f"not expecting duplicate file path: {duplicates}")

        name = self.make_fileset_name(user, files)

        fileset = await self.storage.load(FileSet, name)
        if not fileset:
            fileset = FileSet(
                id=name,
                owner=user.organization,
                changes=[(now, "created")],
                type=mime,
                created=now,
                files=files,
                metadata=metadata,
                state="pending",
            )
        else:
            if fileset.state != "pending":
                raise RuntimeError(
                    "file set cannot be modified after being maked as completed"
                )

            fileset.files = files
            fileset.metadata = metadata
            fileset.type = mime
            fileset.changes.append((now, "update while pending"))

        await self.save(fileset)
        return fileset

    async def load_fileset(self, user, name):
        fileset = await self.storage.load(FileSet, name)

        # validate access
        if fileset and fileset.owner == user.organization:
            return fileset

        return None

    async def make_analysis(self, user, module, inputs):
        now = datetime.now(UTC).replace(microsecond=0)

        args = {}
        for key, value in sorted(inputs.items()):
            if key not in module.inputs:
                raise RuntimeError(f"unexpected input {key}")
            if value.startswith("@"):
                p = value.split("/")
                h = p[0][1:]
                fileset = await self.load_fileset(user, h)
                if not fileset:
                    raise RuntimeError(f"unknown fileset {h}")
                if len(p) > 1:
                    value = fileset.metadata
                    for i in p[1:]:
                        value = value[i]
            args[key] = value

        missing = [
            i for i, arg in module.inputs.items() if i not in args and not arg.optional
        ]
        if len(missing) != 0:
            raise RuntimeError(f"missing required input: {missing}")

        name = self.make_analysis_name(user, module.id, args)

        analysis = await self.load_analysis(user, name)
        if analysis:
            return analysis

        analysis = Analysis(
            id=name,
            owner=user.organization,
            changes=[(now, "created")],
            created=now,
            module=module.id,
            inputs=args,
            state="pending",
        )

        await self.save(analysis)
        await self.storage.save_pending("analysis", name)
        return analysis

    async def load_analysis(self, user, name):
        analysis = await self.storage.load(Analysis, name)

        # validate access
        if analysis and analysis.owner == user.organization:
            return analysis

        return analysis

    async def save(self, resource):
        await self.storage.save(resource.id, resource)

    async def pending(self, what):
        async for item, pending in self.storage.find_pending(what):
            yield item, pending
