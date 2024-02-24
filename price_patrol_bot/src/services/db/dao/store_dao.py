from price_patrol_bot.src.services.db.dao.base_dao import BaseDao
from price_patrol_bot.src.services.db.models import MStore


class StoreDao(BaseDao[MStore]):
    model = MStore
