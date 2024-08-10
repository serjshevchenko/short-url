from urllib import parse as url_parse

from short_url.domain.services.short_url.id_generator import IdGenerator
from short_url.domain.services.short_url.repository import Repository


class ShortUrl:
    def __init__(
        self,
        short_url_tmpl: str,
        id_generator: IdGenerator,
        repository: Repository,
    ) -> None:
        self.id_generator = id_generator
        self.repository = repository
        self.short_url_tmpl = short_url_tmpl

        test_url = short_url_tmpl.format(id="test")
        assert test_url.endswith("/test"), f"Got invalid short_url template: {short_url_tmpl}"

    async def short_url(self, long_url: str) -> str:
        id = await self.id_generator.get_next_id()
        entity = self.repository.create_entity(id, long_url)
        await self.repository.add(entity)
        return self.short_url_tmpl.format(id=id)

    async def resolve_long_url(self, short_url: str) -> str:
        parsed = url_parse.urlparse(short_url)
        id = parsed.path.strip("/").rsplit("/", 1)[1]
        entity = await self.repository.get_by_id(id)
        return entity.long_url
