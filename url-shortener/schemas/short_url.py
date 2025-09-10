from pydantic import BaseModel, AnyHttpUrl

from typing import Annotated

from annotated_types import Len


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str


class ShortUrl(ShortUrlBase):
    pass


class ShortUrlCreate(ShortUrlBase):
    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]
