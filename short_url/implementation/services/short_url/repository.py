from collections.abc import Callable

import aiosqlite

from short_url.domain.services.short_url.repository import Repository, Entity
from .mapper import Mapper, DbRecord


class NotFoundError(Exception):
    def __init__(self, id: str, name: str, msg: str) -> None:
        self.id = id
        self.name = name
        self.message = msg


class DbRepository(Repository):

    def __init__(
        self,
        connection: Callable[..., aiosqlite.Connection],
        mapper: Mapper,
    ) -> None:
        self.connection = connection
        self.mapper = mapper

    async def add(self, entity: Entity) -> None:
        async with self.connection() as db:
            insert_sql = "INSERT INTO long_url (id, long_url, created_at) VALUES (?, ?, ?)"
            db_record = self.mapper.to_db_record(entity)
            await db.execute(insert_sql, db_record)
            await db.commit()

    async def get_by_id(self, id: str) -> Entity:
        async with self.connection() as db:
            cursor = await db.execute(
                "SELECT id, long_url, created_at FROM long_url WHERE id = ?",
                (id,),
            )
            row = await cursor.fetchone()
            if row is None:
                raise NotFoundError(
                    id, "ShortURLEntity", f"Cound not find long url by {id=}",
                )
            return self.mapper.to_entity(DbRecord(*row))
