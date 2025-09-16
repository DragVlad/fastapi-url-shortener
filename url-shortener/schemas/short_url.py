from pydantic import BaseModel, AnyHttpUrl

from typing import Annotated

from annotated_types import Len, MaxLen


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: Annotated[
        str,
        MaxLen(200),
    ] = ""


class ShortUrl(ShortUrlBase):
    slug: str


class ShortUrlCreate(ShortUrlBase):
    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]


class ShortUrlUpdate(ShortUrlBase):
    description: Annotated[
        str,
        MaxLen(200),
    ]
