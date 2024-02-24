from price_patrol_bot.src.services.db.dao.base_dao import BaseDao
from price_patrol_bot.src.services.db.models import MProduct


class ProductDao(BaseDao[MProduct]):
    model = MProduct
