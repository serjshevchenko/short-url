import fastapi

from short_url.api.router import router
from .lifespan import lifespan


def create_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app
