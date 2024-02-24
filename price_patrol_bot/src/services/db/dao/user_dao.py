from sqlalchemy.dialects.sqlite import insert

from price_patrol_bot.src.services.db.dao.base_dao import BaseDao
from price_patrol_bot.src.services.db.models import MUser


class UserDao(BaseDao[MUser]):
    model = MUser

    async def insert_or_nothing(self, user_id: int) -> None:
        query = insert(self.model).values(id=user_id).on_conflict_do_nothing()
        await self._session.execute(query)
        await self._session.commit()
