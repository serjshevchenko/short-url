import typing as t
from collections.abc import Callable

import aiosqlite
import fastapi

from short_url.config import Config
from short_url.domain.services.short_url.short_url import ShortUrl
from short_url.domain.services.short_url.repository import Repository as IRepository
from short_url.implementation.services.short_url.repository import DbRepository
from short_url.implementation.services.short_url.mapper import Mapper


Connect = Callable[..., aiosqlite.Connection]


def get_db(request: fastapi.Request) -> Connect:
    conf: Config = request.app.state.config
    return lambda: aiosqlite.connect(conf.DB_NAME)


def get_short_url_repository(
    db_connect: Connect = fastapi.Depends(get_db),
) -> IRepository:
    return DbRepository(db_connect, Mapper())


def get_short_url_service(
    request: fastapi.Request,
    repo: IRepository = fastapi.Depends(get_short_url_repository),
) -> ShortUrl:
    conf: Config = request.app.state.config
    return ShortUrl(
        id_generator=request.app.state.id_generator,
        repository=repo,
        short_url_tmpl=conf.SHORT_URL_TEMPLATE,
    )


ShortUrlAnnotated = t.Annotated[ShortUrl, fastapi.Depends(get_short_url_service)]
