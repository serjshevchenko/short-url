import fastapi

from .endpoints import router as short_url_router


router = fastapi.APIRouter()
router.include_router(short_url_router)
