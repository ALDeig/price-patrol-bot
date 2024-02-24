from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from price_patrol_bot.src.services.user import response_cmd_start

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: Message):
    text, kb = await response_cmd_start(msg.chat.id)
    await msg.answer(text, reply_markup=kb)


@router.callback_query(
    F.data.startswith("store").as_("data")
    & F.message.func(lambda message: isinstance(message, Message)).as_("message")
)
async def select_store(
    call: CallbackQuery, state: FSMContext, data: str, message: Message
):
    await call.answer()
    store_id = data.split(":")[-1]
    await state.update_data(store_id=int(store_id))
    await state.set_state("get_article_product")
    await message.edit_text("Введите ариткул товара или ссылку на товар")


@router.message(StateFilter("get_article_product"))
async def get_article_product(msg: Message):
    await msg.edit_text("Собираются данные")
