from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field

from dpkit.api import File, FileSet, User
from dpkit.api.server.auth import active_user


class FileSetRequest(BaseModel):
    mime: str | None = Field(
        title="MIME type of the file set. Will autodetect if not set or set to 'auto'.",
        default=None,
    )
    files: list[File] = Field(
        title="Files requested for upload",
    )
    metadata: dict[str, Any] | None = Field(
        title="Associated metadata",
        default=None,
    )


router = APIRouter(prefix="/fileset", tags=["module"])


@router.post("/", summary="Request the creation of a new file set")
async def create_fileset(
    user: Annotated[User, Depends(active_user)],
    args: Annotated[
        FileSetRequest,
        Body(
            examples=[
                {
                    "files": [
                        {
                            "path": "CMU-1.svs",
                            "size": 177552579,
                            "sha1": "da6b71f1ef8365676c385d40dd55f38aa5c726da",
                        }
                    ],
                },
            ],
        ),
    ],
    request: Request,
) -> FileSet:
    """
    A file set has a unique ID that can be specified as input to a module.
    For example:

    - an SVS file would be a file set with 1 file
    - a DICOM file-set (e.g. using a DICOMDIR) would be a file set with multiple files

    When making a request to create a file set, each file of the file set needs to be specified.
    Their size and the SHA-1 of their content must also be supplied.
    The request is idempotent meaning that the same set of files with the same size and SHA-1 will result in the same file set ID.

    ### Push

    By default, the API will use the "push" method.
    This method provides an URL that can be used to upload the file over HTTP.
    If the file is large, multiple URLs will be provided so that the file can be uploaded in parts.
    By default, each part is 32MB.

    Note that those URLS will expire after a short period of time e.g. 1 hour.
    If an URL expires during the upload process, use the idempotent property of the file set creation request.
    Simply redo the exact same request.
    This will return a new set or URLs that can be used to retry uploading any missing part.

    ### Pull

    If access information for a file is specified with the request, it will be used to download the file.
    This is the "pull" method.
    If an URL is specified directly, it needs to be accessible without credentials.
    The other access methods are used to fetch a working copy of the file.

    #### Using HTTP

    The file will be created from the concatenated payload of each URL.
    For example, any kind of authorization built into the URL or specified as headers can be used here.

    - [Sharing objects with presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) for AWS
    - [Delegate access by using a shared access signature](https://learn.microsoft.com/en-us/rest/api/storageservices/delegate-access-with-shared-access-signature) for Azure

    Make sure to monitor the status of the file set for any error that might arise.
    If needed, redo the same request with new URLs.
    Because the file set creation request is idempotent, new URLs will be used to complete any missing parts.

    #### Using Cloud Credentials

    Alternatively, if the request contains credentials from one of the supported cloud provider, those will be used.
    """
    try:
        fileset = await request.app.state.store.make_fileset(
            user=user,
            files=args.files,
            mime=args.mime,
            metadata=args.metadata,
        )
    except RuntimeError as err:
        raise HTTPException(400, str(err))

    return fileset


@router.get("/{id}", summary="Get the uploading status of a file set")
async def get_fileset_status(
    user: Annotated[User, Depends(active_user)],
    id: Annotated[str, Path(title="ID of the file set")],
    request: Request,
) -> FileSet:
    """
    Use this route to monitor the progress of the upload of a file set.
    """
    fileset = await request.app.state.store.load_fileset(user, id)
    if not fileset:
        raise HTTPException(404)

    return fileset


@router.post("/{id}", summary="Complete file set upload")
async def complete_fileset(
    user: Annotated[User, Depends(active_user)],
    id: Annotated[str, Path(title="ID of the file set")],
    request: Request,
) -> None:
    """
    Use this route to notify that the upload of the file set is complete.
    """
    fileset = await request.app.state.store.load_fileset(user, id)
    if not fileset:
        raise HTTPException(404)

    # update the fileset state to indicate it is waiting to be processed
    fileset.state = "completing"
    fileset.changes.append(
        (
            datetime.now(UTC).replace(microsecond=0),
            "received upload complete notification",
        )
    )
    await request.app.state.store.save(fileset)

    # add the fileset to list of work pending
    await request.app.state.store.storage.save_pending("fileset", id)
    return fileset
