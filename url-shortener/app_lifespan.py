from contextlib import asynccontextmanager

from api.api_v1.short_urls.crud import storage

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.init_storage_from_state()
    yield
