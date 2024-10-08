from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field

from dpkit.api import Analysis, User
from dpkit.api.server.auth import active_user


class AnalysisRequest(BaseModel):
    module: str = Field(
        title="ID of the module used to perform the analysis",
    )
    inputs: dict[str, Any] = Field(
        title="Inputs to be supplied to the module",
    )
    account: str | None = Field(
        title="ID of an account (e.g. customer) for accounting",
        default=None,
    )


router = APIRouter(prefix="/analysis", tags=["module"])


@router.post("/", summary="Request an analysis")
async def module_analysis_request(
    user: Annotated[User, Depends(active_user)],
    args: Annotated[
        AnalysisRequest,
        Body(
            title="Analysis request",
            examples=[
                {
                    "module": "prostate-detect:1.2.3",
                    "inputs": {
                        "wsi": "@da6b71f1ef8365676c385d40dd55f38aa5c726da",
                        "stain": "@da6b71f1ef8365676c385d40dd55f38aa5c726da/stain",
                    },
                },
            ],
        ),
    ],
    request: Request,
) -> Analysis:
    """
    Use this route to schedule the analysis of a set of inputs by a module.

    The inputs is used to invoke the specified module for this request with either literal values or file set IDs.
    File set IDs should be prefixed with "@".
    If the file set ID is followed by a path, the content will be replaced by the file set metadata value associated with that path.
    Every required inputs of the module need to be set and exist for the analysis to be created.
    All file set needs to be completed for the analysis to be scheduled.
    Once scheduled, use the analysis status route to monitor its progress.
    """
    module = request.app.state.modules.get(args.module)
    if not module:
        raise HTTPException(400, f"unknown module: {args.module}")

    try:
        analysis = await request.app.state.store.make_analysis(
            user=user,
            module=module,
            inputs=args.inputs,
        )
    except RuntimeError as err:
        raise HTTPException(400, str(err))

    return analysis


@router.get("/{id}", summary="Get analysis status")
async def analysis_status(
    user: Annotated[User, Depends(active_user)],
    id: Annotated[str, Path(title="ID of the analysis")],
    request: Request,
) -> Analysis:
    """
    Use this route to monitor the progress of an analysis.

    Once a request completes successfully, results will be populated and file sets available for download if needed.
    Each result is either literal values or file set IDs that can be used as inputs to other modules.
    Note that if authorization delegation is enabled, the URL for each file expires after a short period of time e.g. 1 hour.
    Simply use this route again to get a new set of URLs and retry any failed download.
    """
    return await request.app.state.store.load_analysis(user, id)
