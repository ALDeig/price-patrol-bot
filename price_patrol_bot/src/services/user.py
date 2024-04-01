from aiogram.types import InlineKeyboardMarkup

from price_patrol_bot.src.dialogs.keyboards.trackings import kb_select_store
from price_patrol_bot.src.services.db.base import session_factory
from price_patrol_bot.src.services.db.dao.store_dao import StoreDao
from price_patrol_bot.src.services.db.dao.user_dao import UserDao


async def response_cmd_start(user_id: int) -> tuple[str, InlineKeyboardMarkup | None]:
    async with session_factory() as session:
        await UserDao(session).insert_or_nothing(user_id)
        stores = await StoreDao(session).find_all()
    kb = kb_select_store(stores) if stores else None
    text = (
        "Этот бот поможет отслеживать цену на товар. "
        "Выберите маркетплейс на котором нужно отследить товар:"
    )
    return text, kb
