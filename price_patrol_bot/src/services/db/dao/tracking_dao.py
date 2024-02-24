from price_patrol_bot.src.services.db.dao.base_dao import BaseDao
from price_patrol_bot.src.services.db.models import MTracking


class TrackingDao(BaseDao[MTracking]):
    model = MTracking
