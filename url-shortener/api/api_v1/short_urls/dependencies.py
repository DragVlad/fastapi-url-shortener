import logging

from typing import Annotated

from schemas.short_url import ShortUrl
from .crud import storage
from core.config import API_TOKENS

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Header,
    status,
)

log = logging.getLogger(__name__)


UNSAVE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def prefetch_short_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    yield
    if request.method in UNSAVE_METHODS:
        log.info("Add background task to save storage")
        background_tasks.add_task(storage.save_state)


def api_token_required(
    request: Request,
    api_token: Annotated[
        str,
        Header(alias="x-auth-token"),
    ] = "",
):
    if request.method not in UNSAVE_METHODS:
        return
    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
