import fastapi

from . import deps


router = fastapi.APIRouter()


@router.post("/short-url", response_model=str)
async def gen_short_url(
    short_url: deps.ShortUrlAnnotated,
    long_url: str = fastapi.Body(embed=True),
) -> str:
    return await short_url.short_url(long_url)


@router.get("/go/{id}", response_model=str)
async def resolve_long_url(
    short_url: deps.ShortUrlAnnotated,
    request: fastapi.Request,
) -> str:
    return await short_url.resolve_long_url(str(request.url))
