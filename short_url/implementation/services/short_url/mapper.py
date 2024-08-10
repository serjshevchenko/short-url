import datetime as dt
import typing as t

from short_url.domain.services.short_url.mapper import Mapper as _Mapper
from short_url.domain.services.short_url.repository import Entity


class DbRecord(t.NamedTuple):
    id: str
    long_url: str
    created_at: dt.datetime


class Mapper(_Mapper[DbRecord]):

    @staticmethod
    def to_entity(db_record: DbRecord) -> Entity:
        return Entity(
            id=db_record.id,
            long_url=db_record.long_url,
            created_at=db_record.created_at,
        )

    @staticmethod
    def to_db_record(entity: Entity) -> DbRecord:
        return DbRecord(
            id=entity.id,
            long_url=entity.long_url,
            created_at=entity.created_at,
        )
