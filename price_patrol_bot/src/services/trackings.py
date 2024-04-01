from price_patrol_bot.src.services.db.base import session_factory
from price_patrol_bot.src.services.db.models import MTracking
from price_patrol_bot.src.services.parsers.base_parser import Parser
from price_patrol_bot.src.services.parsers.wb import WBParser
from price_patrol_bot.src.services.products import Product
from price_patrol_bot.src.services.db.dao.tracking_dao import TrackingDao


class CreateTracking:
    def __init__(self, store_id: int, article_or_url: str) -> None:
        self._store_id = store_id
        self._article = article_or_url
        self._product = Product(store_id, article_or_url)

    async def save_tracking(self) -> str:
        product = await self._product.get_product()
        async with session_factory() as session:
            dao = TrackingDao(session)
            await dao.add(MTracking())
        
        parser = self._get_parser()
        product = await parser.get_product()
        return f"{product.name} - {product.price}"

    def _get_parser(self) -> Parser:
        parsers = {1: WBParser}
        parser = parsers[self._store_id]
        return parser(self._article)
