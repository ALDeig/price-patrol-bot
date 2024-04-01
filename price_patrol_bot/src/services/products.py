from price_patrol_bot.src.services.db.base import session_factory
from price_patrol_bot.src.services.db.dao.product_dao import ProductDao
from price_patrol_bot.src.services.parsers.base_parser import Parser, ProductData
from price_patrol_bot.src.services.parsers.wb import WBParser
from price_patrol_bot.src.services.stores import Stores


class Product:
    def __init__(self, store_id: int, article_or_url: str, parser: Parser) -> None:
        self.store_id = store_id
        self._parser = parser
        self.article = self._parser.article

    async def get_old_product(self) -> ProductData:
        async with session_factory() as session:
            product_db = await ProductDao(session).find_one_or_none(
                store=self.store_id, article=self.article
            )
            if product_db:
                return ProductData.model_validate(product_db)
        return await self._parser.get_product()

    async def get_new_product(self) -> ProductData:
        return await self._parser.get_product()

    async def update_product(self):
        ...

    async def _save_product(self):
        ...

    def _get_parser(self, article_or_url: str) -> Parser:
        parsers = {Stores.WILDBERRIES.value: WBParser}
        parser = parsers[self.store_id]
        return parser(article_or_url)
