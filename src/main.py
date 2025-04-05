from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from src.handlers import register_handlers
from src.markups import main_menu
from src.config import config


dp = Dispatcher()


@dp.message(Command("start", "help", "menu"))
async def command_start_handler(message: Message):
    await message.answer(
        "Головне меню",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu
    )


async def main():
    print("Ready")
    register_handlers(dp)
    bot = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
