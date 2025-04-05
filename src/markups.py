from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Створити статтю"),
        KeyboardButton(text="Отримати статті")
    ],
    [
        KeyboardButton(text="Редагувати статтю"),
        KeyboardButton(text="Видалити статтю")
    ]
], resize_keyboard=True)

cancel_markup = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Скасувати")
]], resize_keyboard=True)
