from pathlib import Path

from dpkit.api.app import make_app
from dpkit.api.store import Store

app = make_app(Store(root=Path.cwd()), {}, [])
