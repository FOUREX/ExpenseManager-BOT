from datetime import datetime

from aiogram import Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.markups import main_menu, cancel_markup
from src.expense_manager import expense_manager


router = Router()
get_date_now = lambda: datetime.today().strftime("%d.%m.%Y")


class CreateExpenseState(StatesGroup):
    name = State()
    created_at = State()
    amount = State()


async def cancel(message: Message, state: FSMContext):
    await message.answer("Головне меню", reply_markup=main_menu)
    await state.clear()


@router.message(F.text == "Створити статтю")
async def create_expense(message: Message, state: FSMContext):
    await message.answer(
        f"Введіть назву статті",
        reply_markup=cancel_markup
    )
    await state.set_state(CreateExpenseState.name)


@router.message(CreateExpenseState.name)
async def create_expense_name(message: Message, state: FSMContext):
    if message.text == "Скасувати":
        return await cancel(message, state)

    await state.update_data(name=message.text)
    await message.answer(
        f"Введіть дату, наприклад: `{get_date_now()}`",
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(CreateExpenseState.created_at)


@router.message(CreateExpenseState.created_at)
async def create_expense_created_at(message: Message, state: FSMContext):
    if message.text == "Скасувати":
        return await cancel(message, state)

    try:
        date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer(
            f"Не коректна дата\nВведіть дату, наприклад: `{get_date_now()}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await state.update_data(created_at=date)
    await message.answer(
        f"Введіть суму витрат у гривнях",
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(CreateExpenseState.amount)


@router.message(CreateExpenseState.amount)
async def create_expense_amount(message: Message, state: FSMContext):
    if message.text == "Скасувати":
        return await cancel(message, state)

    try:
        amount = int(float(message.text.replace(",", ".")) * 100) / 100
    except ValueError:
        await message.answer(
            f"Не коректний формат суми, спробуйте знову",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if amount >= 1_000_000_000_000_000:
        await message.answer(
            "Сума не повинна перевищувати п'ятнадцяти знаків цілої частини та двох знаків дробової. Спробуйте знову"
        )
        return

    data = await state.get_data()
    await state.clear()

    result = await expense_manager.create_expense(
        name=data["name"],
        created_at=data["created_at"],
        amount=amount,
    )

    await message.answer(
        f"*Створена стаття:*\n"
        f"ID: `{result.id}`\n"
        f"Назва: `{result.name}`\n"
        f"Сума витрат: `{result.amount_uah}₴` | `{result.amount_usd}$`\n"
        f"Дата: `{datetime.fromisoformat(result.created_at.replace("Z", "+00:00")).strftime("%d.%m.%Y")}`",
        reply_markup=main_menu,
        parse_mode=ParseMode.MARKDOWN
    )


def register(dp: Dispatcher):
    dp.include_router(router)
