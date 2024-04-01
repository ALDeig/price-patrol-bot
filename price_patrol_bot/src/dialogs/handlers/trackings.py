from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


router = Router()


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
    await message.edit_text("Введите ариткул/код товара или ссылку на товар")


@router.message(StateFilter("get_article_product"), F.text.as_("text"))
async def get_article_product(msg: Message, text: str):
    await msg.edit_text("Собираются данные")
