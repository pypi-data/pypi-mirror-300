from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request

from dpkit.api import Module, User
from dpkit.api.server.auth import active_user

router = APIRouter(prefix="/module", tags=["module"])


@router.get("/", summary="List available modules")
async def module_list(
    user: Annotated[User, Depends(active_user)],
    request: Request,
) -> list[str]:
    """
    Use this route to get the list of available modules.
    """
    return list(request.app.state.modules.keys())


@router.get("/{id}", summary="Get module details")
async def module_details(
    user: Annotated[User, Depends(active_user)],
    id: Annotated[str, Path(title="ID of the module")],
    request: Request,
) -> Module:
    """
    Use this route to get information about a module e.g. description, inputs.

    Each input has a name, a type and a list of supported formats.
    The name is used when requesting an analysis to specify the value of an input.

    ## Literal Types

    The following indicates details about supported types:

    #### number

    Indicates a number.

    #### string

    Indicates a string without internationalization.

    #### text

    Indicates a dictionnary of [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) (2 letter codes) to its corresponding text.

    #### roi

    Indicates a region of interest.
    Specify the origin as `x,y` and the size as `w,h` using the format `x,y-w,h`.

    ## Reference Types

    Use [MIME](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/) type.

    #### WSI

    Indicates a reference to a whole slide image (WSI) such as:

    - application/dicom
    - application/vnd.philips.isyntax
    - application/vnd.philips.isyntax2
    - image/jpeg
    - image/png
    - image/tiff
    - image/tiff; format=ndpi
    - image/tiff; format=ome
    - image/tiff; format=svs

    The following metadata can be specified:

    - staining
    - specimen
    - mpp
    - device

    #### Overlays

    Overlays are numerical and/or categorical values associated with a WSI image.

    - application/vnd.numpy.npy
    - application/vnd.numpy.npz
    - application/vnd.pytorch.pth
    - application/x-hdf5
    - application/x-parquet
    - application/x-safetensors

    #### Structured Data

    - application/json
    - application/xml
    - text/csv
    - text/yaml
    """
    module = request.app.state.modules.get(id)
    if not module:
        raise HTTPException(404)

    return module
