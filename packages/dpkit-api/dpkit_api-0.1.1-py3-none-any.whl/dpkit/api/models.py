from datetime import datetime
from typing import Any

from pydantic import AnyUrl, BaseModel, Field


class User(BaseModel):
    id: str = Field(
        title="Unique ID of a user",
    )
    organization: str = Field(
        title="Name of the organization of this user",
    )
    disabled: bool = Field(
        title="Indicate if user is disabled",
        default=False,
    )


class Resource(BaseModel):
    id: str = Field(
        title="ID of the resource",
    )
    owner: str | None = Field(
        title="ID of the organization that can access this resource",
        default=None,
    )
    created: datetime | None = Field(
        title="Date/Time when this resource was created",
        default=None,
    )
    changes: list[tuple[datetime, str]] | None = Field(
        title="Date/Time when this resource was updated with information about the change",
        default=None,
    )


class FilePart(BaseModel):
    url: str = Field(
        title="URL to upload/download this file part over HTTP",
    )
    headers: dict[str, str] | None = Field(
        title="Additional headers to include in the request for this part",
        default=None,
    )
    status: str = Field(
        title="Status of this file part",
    )


class UsingHTTP(BaseModel):
    name: str = "http"
    parts: list[FilePart] = Field(
        title="List of file parts to limit the size of individual HTTP request",
    )
    headers: dict[str, str] | None = Field(
        title="Additional headers to include in the request",
        default=None,
    )


class UsingAWS(BaseModel):
    name: str = "aws"
    bucket: str = Field(
        title="Name of the S3 bucket",
    )
    object: str = Field(
        title="Name of the object",
    )
    access: str = Field(
        title="Access key ID (AWS_ACCESS_KEY_ID)",
    )
    secret: str = Field(
        title="Secret access key (AWS_SECRET_ACCESS_KEY)",
    )
    session: str | None = Field(
        title="Session token (AWS_SESSION_TOKEN)",
        default=None,
    )
    region: str = Field(
        title="Name of the region (AWS_REGION)",
    )


class UsingAzure(BaseModel):
    name: str = "azure"
    storage: str = Field(
        title="Name of the storage account",
    )
    container: str = Field(
        title="Name of the container",
    )
    blob: str = Field(
        title="Name of the blob",
    )
    application: str = Field(
        title="ID of the application of the service principal's app registration (AZCOPY_SPA_APPLICATION_ID)",
    )
    secret: str = Field(
        title="Client secret of the application (AZCOPY_SPA_CLIENT_SECRET)",
    )
    tenant: str = Field(
        title="ID of the tenant in the Azure portal (AZCOPY_TENANT_ID)",
    )


class File(BaseModel):
    path: str = Field(
        title="File path relative to its set",
        max_length=128,
    )
    size: int = Field(
        title="File size in bytes",
    )
    sha1: str = Field(
        title="File SHA-1 digest encoded as hexadecimal digits",
        pattern="[a-f0-9]{40}",
    )
    access: AnyUrl | UsingHTTP | UsingAWS | UsingAzure | None = Field(
        title="File location URL or indications on how to access the file",
        default=None,
    )
    state: str | None = Field(
        title="State of this file",
        default=None,
    )


class FileSet(Resource):
    type: str | None = Field(
        title="Type of the file set",
    )
    files: list[File] = Field(
        title="Files associated to this set",
    )
    metadata: dict[str, Any] | None = Field(
        title="Associated metadata",
    )
    state: str = Field(
        title="State of this file set",
    )


class Analysis(Resource):
    module: str = Field(
        title="ID of the module that produces the analysis",
    )
    inputs: dict[str, Any] = Field(
        title="Inputs supplied to the module",
    )
    state: str = Field(
        title="Current status",
    )
    results: dict[str, Any] | None = Field(
        title="If available, results produced by the module",
        default=None,
    )


class Details(BaseModel):
    types: list[str] = Field(
        title="Supported types for the input argument",
    )
    description: str | None = Field(
        title="Description of the input",
        default=None,
    )
    optional: bool | None = Field(
        title="Set if this input is optional",
        default=False,
    )


class Module(BaseModel):
    id: str = Field(
        title="ID of the module",
    )
    inputs: dict[str, Details] = Field(
        title="Information about the module inputs",
    )
    description: str | None = Field(
        title="Description of the module",
        default=None,
    )
