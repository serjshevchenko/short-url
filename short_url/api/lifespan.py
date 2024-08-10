from contextlib import asynccontextmanager

import fastapi
import typing as t

from short_url.config import config

from short_url.domain.services.short_url.id_generator import IdGenerator


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> t.AsyncGenerator[None, None]:
    app.state.config = config
    app.state.id_generator = IdGenerator(
        node_id=config.NODE_ID,
    )
    yield
    del app.state.id_generator
