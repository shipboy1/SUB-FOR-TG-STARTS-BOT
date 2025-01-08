from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_sub_category

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Профиль', callback_data='profile')],
                                                       [InlineKeyboardButton(text='Категории подписки', callback_data='categories')],
                                                       [InlineKeyboardButton(text='Поддержка', callback_data='support')]])

back_to_home = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Главная', callback_data='home')]])

pay_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Перейти к оплате', callback_data='go_to_pay')],
                                                     [InlineKeyboardButton(text='Главная', callback_data='home')]])

channel_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Основной канал')]], resize_keyboard=True)

async def inline_categories(callback_data):
    builder = InlineKeyboardBuilder()
    all_categories = await get_sub_category()
    for category in all_categories:
        builder.add(InlineKeyboardButton(text=category.name, callback_data=f'item_{category.id}'))
    builder.add(InlineKeyboardButton(text='Назад', callback_data=callback_data))
    return builder.adjust(2).as_markup()

def star_pay():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Оплатить 1 ⭐️', pay=True)) # вместо 
    builder.add(InlineKeyboardButton(text='На главную', callback_data='home'))
    return builder.adjust(1).as_markup()