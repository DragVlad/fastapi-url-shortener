from typing import Annotated
from schemas.short_url import ShortUrl

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import (
    RedirectResponse,
)


app = FastAPI(
    title="URL Shortener",
)


SHORT_URLS = [
    ShortUrl(
        target_url="https://example.com",
        slug="example",
    ),
    ShortUrl(
        target_url="https://google.com",
        slug="search",
    ),
]


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
    )
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


@app.get(
    "/short-urls",
    response_model=list[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


def prefetch_short_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = next(
        (url for url in SHORT_URLS if url.slug == slug),
        None,
    )
    if url:
        return RedirectResponse(
            url=url.target_url,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
):
    return RedirectResponse(
        url=url.target_url,
    )


@app.get(
    "/short-urls/{slug}",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortUrl:
    return url
