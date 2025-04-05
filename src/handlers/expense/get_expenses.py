from datetime import datetime, timedelta

from aiogram import Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.markups import main_menu, cancel_markup
from src.utils import expenses_to_xlsx_file
from src.expense_manager import expense_manager


router = Router()
get_date_now = lambda: datetime.today().strftime("%d.%m.%Y")


class GetExpenseState(StatesGroup):
    start_date = State()
    end_date = State()


async def cancel(message: Message, state: FSMContext):
    await message.answer("Головне меню", reply_markup=main_menu)
    await state.clear()


@router.message(F.text == "Отримати статті")
async def get_expense(message: Message, state: FSMContext):
    await message.answer(
        f"Введіть початкову дату, наприклад: `{get_date_now()}`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=cancel_markup
    )
    await state.set_state(GetExpenseState.start_date)


@router.message(GetExpenseState.start_date)
async def get_expense_start_date(message: Message, state: FSMContext):
    if message.text == "Скасувати":
        return await cancel(message, state)

    try:
        date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer(
            f"Не коректна дата\nВведіть початкову дату, наприклад: `{get_date_now()}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await state.update_data(start_date=date)
    await message.answer(
        f"Введіть кінцеву дату, наприклад: `{get_date_now()}`",
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(GetExpenseState.end_date)


@router.message(GetExpenseState.end_date)
async def get_expense_end_date(message: Message, state: FSMContext):
    if message.text == "Скасувати":
        return await cancel(message, state)

    try:
        date = datetime.strptime(message.text, "%d.%m.%Y") + timedelta(hours=23, minutes=59, seconds=59)
    except ValueError:
        await message.answer(
            f"Не коректна дата\nВведіть кінцеву дату, наприклад: `{get_date_now()}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await state.update_data(end_date=date)
    data = await state.get_data()
    await state.clear()

    expenses = await expense_manager.get_expenses(start_date=data["start_date"], end_date=data["end_date"])
    file = expenses_to_xlsx_file(expenses)

    await message.answer_document(
        caption="_Для розрахунку загальних сум витрат може знадобитися увімкнення редагування_",
        document=BufferedInputFile(
            file.read(), filename=f"expenses_{data["start_date"].date()}_{data["end_date"].date()}.xlsx"
        ),
        reply_markup=main_menu,
        parse_mode=ParseMode.MARKDOWN
    )


def register(dp: Dispatcher):
    dp.include_router(router)
