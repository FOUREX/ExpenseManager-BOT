from datetime import datetime

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


class DeleteExpenseState(StatesGroup):
    id = State()
    name = State()
    amount = State()


async def cancel(message: Message, state: FSMContext):
    await message.answer("Головне меню", reply_markup=main_menu)
    await state.clear()


@router.message(F.text == "Видалити статтю")
async def delete_expense(message: Message, state: FSMContext):
    expenses = await expense_manager.get_expenses()
    file = expenses_to_xlsx_file(expenses)

    await message.answer_document(
        caption="Введіть ID статті яку потрібно видалити",
        reply_markup=cancel_markup,
        document=BufferedInputFile(
            file.read(), filename=f"expenses.xlsx"
        )
    )
    await state.set_state(DeleteExpenseState.id)


@router.message(DeleteExpenseState.id)
async def edit_expense_id(message: Message, state: FSMContext):
    if message.text == "Скасувати":
        return await cancel(message, state)

    try:
        id = int(message.text)
    except ValueError:
        await message.answer("Не коректний формат: ID повинен бути цілим числом. Спробуйте знову")
        return

    expense = await expense_manager.delete_expense(id)

    if expense is None:
        await message.answer(f"Статті з ID {id} не знайдено, спробуйте знову")
        return

    await state.update_data(id=id)
    await message.answer(
        f"*Видалена стаття:*\n"
        f"ID: `{expense.id}`\n"
        f"Назва: `{expense.name}`\n"
        f"Сума витрат: `{expense.amount_uah}₴` | `{expense.amount_usd}$`\n"
        f"Дата: `{datetime.fromisoformat(expense.created_at.replace("Z", "+00:00")).strftime("%d.%m.%Y")}`",
        reply_markup=main_menu,
        parse_mode=ParseMode.MARKDOWN
    )
    await state.set_state(DeleteExpenseState.name)


def register(dp: Dispatcher):
    dp.include_router(router)
