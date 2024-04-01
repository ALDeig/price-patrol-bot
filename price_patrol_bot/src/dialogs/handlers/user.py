from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from price_patrol_bot.src.services.user import response_cmd_start

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    await state.clear()
    text, kb = await response_cmd_start(msg.chat.id)
    await msg.answer(text, reply_markup=kb)
