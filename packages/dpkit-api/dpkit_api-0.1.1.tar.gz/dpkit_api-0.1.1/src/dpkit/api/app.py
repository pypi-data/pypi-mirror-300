from fastapi import FastAPI

from dpkit.api.server import analysis, auth, fileset, module
from dpkit.api.version import __version__

description = """
## Overview

Here is the usual sequence of events:

- Create file sets that will be required by the module.
- Request a module to produce a new results.
- Wait for those results to become available for download.
- Download results.
"""


def make_app(store, modules, users):
    tags = [
        {
            "name": "module",
            "description": "Specialized AI models designed for specific tasks",
        },
    ]

    app = FastAPI(
        title="Module API for Pathology",
        description=description,
        version=__version__,
        root_path="/v1",
        openapi_tags=tags,
    )

    app.include_router(auth.router)
    app.include_router(fileset.router)
    app.include_router(module.router)
    app.include_router(analysis.router)

    app.state.store = store
    app.state.modules = modules
    app.state.users = users
    return app
