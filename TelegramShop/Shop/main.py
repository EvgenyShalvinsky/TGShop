import asyncio
import config
import logging
import start
import sql
import util
import text
import keyboards
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=config.Token)
#loop = asyncio.get_event_loop()
storage = MemoryStorage()
# Диспетчер
dp = Dispatcher(bot, storage=storage)

# Подключение к БД
db = sql.sql_start()


problemkb = InlineKeyboardMarkup(row_width=1)
problem_chbtn = InlineKeyboardButton(text='Изменить', callback_data='data_change')
problem_tbtn = InlineKeyboardButton(text='Поддержка', callback_data='payout_help')
problemkb.add(problem_chbtn).add(problem_tbtn)


addgoodkb = InlineKeyboardMarkup(row_width=1)
addgoodkb_btn = InlineKeyboardButton(text='Добавить в корзину', callback_data='good_add')
addgoodkb.add(addgoodkb_btn)




@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await bot.send_message(731620137, text='Пользователь : '+str(message.from_user.id)+' подключился')
    sql.add_user(
        db,
        str(message.from_user.id),
        str(message.from_user.first_name),
        '@'+str(message.from_user.username),
        str(message.from_user.language_code),
        util.get_date()
    )
    print(util.get_date(), 'Команда старт от', str(message.from_user.id))
    await message.answer(text.start_message,
                         reply_markup=keyboards.MainKeyBoard())

@dp.message_handler()
async def kb_answer(message: types.Message):
    if message.text == '🎫Каталог🎲🎭':
        print(util.get_date(), 'Запрос каталога от ', str(message.from_user.id))
        for gn in sql.get_good_name(db):
            print(gn)
            good_name = gn[0]
            print(good_name)
            good_number = str(sql.get_by_number_name(db, str(good_name)))
            print(good_number)
            photo = str(config.GOODS_IMG_PATH)+str(good_number)+'.jpeg'
            print(photo)
            good_price = str(sql.get_price_by_number(db, good_number))
            print(good_price)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=open(photo, 'rb')
            )
            await bot.send_message(
                message.from_user.id,
                text=str(good_name)+'\nЦена : '+str(good_price),
                reply_markup=addgoodkb
            )

    elif message.text == '🎩Корзина📑⚖':
        print(util.get_date(), 'Запрос правил от ', str(message.from_user.id))
        await bot.send_message(message.from_user.id, text='Список покупок : ')
        print(util.get_date(), 'Запрос каталога от ', str(message.from_user.id))
        for good_number in sql.get_good_name(db):
            print(good_number)
            photo = str(config.GOODS_IMG_PATH) + str(good_number) + '.jpeg'
            good_name = str(sql.get_name_by_number(db, int(good_number)))
            good_price = str(sql.get_price_by_number(db, int(good_number)))
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=open(photo, 'rb')
            )
            await bot.send_message(
                message.from_user.id,
                text=str(good_name) + '\nЦена : ' + str(good_price),
                reply_markup=addgoodkb
            )

    if message.text == '💵Заказ💼🏧':
        print(util.get_date(), 'Запрос баланса от ', str(message.from_user.id))

    if message.text == '💵Профиль💼🏧':
        id = str(message.from_user.id)
        zakaz_number = str(sql.get_zakaz_by_id(db, id))
        await message.answer(text="\nПользователь : "+id+
                             "\nАктивный заказ : "+zakaz_number+
                             "\nАдрес доставки: ",
                             reply_markup=problemkb)
        print(util.get_date(), 'Запрос баланса от ', str(message.from_user.id))


@dp.callback_query_handler(lambda cbq: cbq.data == 'good_add')
async def pay_in(callback: types.CallbackQuery):
    print(callback.from_user.values)
    await bot.send_message(callback.from_user.id, text='Введите команду '
                                                 '\n/pay  ٩(◕‿◕｡)۶')

# Запуск процесса поллинга новых апдейтов
async def main():

    await dp.start_polling(bot)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start.start_info()
    sql.create_tables(db)
    sql.add_test_goods(db)
    # loop.create_task(lotto_scheduler())
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
