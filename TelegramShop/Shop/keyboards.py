from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


# Главная клавиатура
def MainKeyBoard():
    mainkb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="🎫Каталог🎲🎭"),
                types.KeyboardButton(text="🎩Корзина📑⚖"),
                types.KeyboardButton(text="💵Заказ💼🏧"),
                types.KeyboardButton(text="💵Профиль💼🏧")
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню :"
    )
    return mainkb

def problemkb():

    return problemkb


paykb = InlineKeyboardMarkup(row_width=1)
paybtn = InlineKeyboardButton(text='Купить', callback_data='pay')

problemkb = InlineKeyboardMarkup(row_width=1)
problem_paybtn = InlineKeyboardButton(text='пополнением ', callback_data='pay_help')
problem_ticketbtn = InlineKeyboardButton(text='покупка билета', callback_data='ticket_help')
problem_lotobtn = InlineKeyboardButton(text='розыгрыш', callback_data='loto_help')
problem_payoutbtn = InlineKeyboardButton(text='вывод', callback_data='payout_help')
problemkb.add(problem_paybtn).add(problem_ticketbtn).add(problem_lotobtn).add(problem_payoutbtn)
