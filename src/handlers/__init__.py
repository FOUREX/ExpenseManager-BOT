from aiogram import Dispatcher

from src.handlers.expense import register as register_expense_handlers


def register_handlers(dp: Dispatcher):
    register_expense_handlers(dp)
