from __future__ import annotations

import dataclasses as dc
import datetime as dt


@dc.dataclass(kw_only=True)
class Entity:
    id: str
    long_url: str
    created_at: dt.datetime


class Repository:

    @staticmethod
    def create_entity(
        id: str, long_url: str, created_at: dt.datetime = dt.datetime.now(dt.UTC),
    ) -> Entity:
        return Entity(id=id, long_url=long_url, created_at=created_at)

    async def add(self, entity: Entity) -> None:
        raise NotImplementedError

    async def get_by_id(self, id: str) -> Entity:
        raise NotImplementedError
