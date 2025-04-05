from aiogram import Dispatcher

from src.handlers.expense.get_expenses import register as get_expense_handlers
from src.handlers.expense.create_expense import register as create_expense_handlers
from src.handlers.expense.edit_expense import register as edit_expense_handlers
from src.handlers.expense.delete_expense import register as delete_expense_handlers


def register_handlers(dp: Dispatcher):
    get_expense_handlers(dp)
    create_expense_handlers(dp)
    edit_expense_handlers(dp)
    delete_expense_handlers(dp)


def register(dp: Dispatcher):
    register_handlers(dp)
