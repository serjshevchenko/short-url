from short_url.domain.services.short_url.repository import Entity


class Mapper[T]:

    @staticmethod
    def to_entity(db_record: T) -> Entity:
        raise NotImplementedError

    @staticmethod
    def to_db_record(entity: Entity) -> T:
        raise NotImplementedError
