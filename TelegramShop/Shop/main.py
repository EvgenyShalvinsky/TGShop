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
logging.basicConfig(level=logging.INFO, filename=config.LOG_FILENAME,filemode="w")

# Объект бота
bot = Bot(token=config.Token)
#loop = asyncio.get_event_loop()
storage = MemoryStorage()
# Диспетчер
dp = Dispatcher(bot, storage=storage)

# Подключение к БД
db = sql.connect()


problemkb = InlineKeyboardMarkup(row_width=1)
problem_chbtn = InlineKeyboardButton(text='Изменить', callback_data='data_change')
problem_tbtn = InlineKeyboardButton(text='Поддержка', callback_data='payout_help')
problemkb.add(problem_chbtn).add(problem_tbtn)


addgoodkb = InlineKeyboardMarkup(row_width=1)
addgoodkb_btn = InlineKeyboardButton(text='/b ', callback_data='/b')
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
    util.write_log('Команда старт от'+str(message.from_user.id))
    await message.answer(text.start_message,
                         reply_markup=keyboards.MainKeyBoard())

@dp.message_handler(commands=['b'])
async def add_to_busket(message: types.Message):
    if message.get_args():
        good_num = int(message.get_args())
        user_id = message.from_user.id
        sql.put_good_in_busket(db, str(user_id), good_num)
        await bot.send_message(message.from_user.id, text='\nТовар : '+str(good_num)+' добавлен в корзину')
    else:
        await bot.send_message(message.from_user.id, text='\nвведите /b и код товара,'
                                                          ' чтобы добавить товар в корзину (пример /b 1001)')
        if int(sql.is_busket(db, str(message.from_user.id))) == 0:
            await bot.send_message(message.from_user.id, text='Ваша корзина пуста')
        else:
            busket_sum = 0
            tovars = sql.get_goodnum_by_user(db, int(message.from_user.id))
            await bot.send_message(message.from_user.id, text='В ваша корзине: ')
            for tv in tovars:
                good_number = tv[0]
                print(good_number)
                cost = str(sql.get_price_by_number(db, int(good_number)))
                print(cost)
                busket_sum = busket_sum + int(cost)
                print(busket_sum)
                name = sql.get_name_by_number(db, int(good_number))
                count = sql.get_count_goods_in_busket(db, int(good_number))
                await bot.send_message(message.from_user.id, text='\n'+str(name)+'\nв кол-ве : '+str(count))
            await bot.send_message(message.from_user.id, text='\nНа сумму : ' + str(busket_sum))

@dp.message_handler(commands=['с'])
async def add_to_busket(message: types.Message):
    for gn in sql.get_good_name(db):
        good_name = gn[0]
        good_number = str(sql.get_by_number_name(db, str(good_name)))
        photo = str(config.GOODS_IMG_PATH) + str(good_number) + '.jpeg'
        good_price = str(sql.get_price_by_number(db, good_number))
        good_description = str(sql.get_decs_by_number(db, good_number))
        bot_msg = str(good_name) + '\nКод :' \
                  + str(good_number) + '\nЦена : ' \
                  + str(good_price) + '\nОписание : ' \
                                      '\n' + str(good_description)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=open(photo, 'rb')
        )
        await bot.send_message(
            message.from_user.id,
            text=bot_msg,
            reply_markup=addgoodkb
        )


@dp.message_handler()
async def kb_answer(message: types.Message):
    if message.text == '🎫Каталог🎲🎭':
        print(util.get_date(), 'Запрос каталога от ', str(message.from_user.id))
        for gn in sql.get_good_name(db):
            good_name = gn[0]
            good_number = str(sql.get_by_number_name(db, str(good_name)))
            photo = str(config.GOODS_IMG_PATH)+str(good_number)+'.jpeg'
            good_price = str(sql.get_price_by_number(db, good_number))
            good_description = str(sql.get_decs_by_number(db, good_number))
            bot_msg = str(good_name)+'\nКод :'\
                      +str(good_number)+'\nЦена : '\
                      +str(good_price)+'\nОписание : '\
                      '\n'+str(good_description)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=open(photo, 'rb')
            )
            await bot.send_message(
                message.from_user.id,
                text=bot_msg,
            )
            await bot.send_message(
                message.from_user.id,
                text='\nВведите /b '+str(good_number)+'\nчто бы добавить товар в корзину')
    elif message.text == '🎩Корзина📑⚖':
        if int(sql.is_busket(db, str(message.from_user.id))) == 0:
            await bot.send_message(message.from_user.id, text='Ваша корзина пуста')
        else:
            tovars = sql.get_goodnum_by_user(db, int(message.from_user.id))
            await bot.send_message(message.from_user.id, text='В ваша корзине: ')
            for tv in tovars:
                tovar = tv[0]
                name = sql.get_name_by_number(db, int(tovar))
                count = sql.get_count_goods_in_busket(db, int(tovar))
                await bot.send_message(message.from_user.id, text='\n'+str(name)+'\nв кол-ве : '+str(count))
    elif message.text == '💵Заказ💼🏧':
        print(util.get_date(), 'Запрос баланса от ', str(message.from_user.id))
    elif message.text == '💵Профиль💼🏧':
        id = str(message.from_user.id)
        zakaz_number = str(sql.get_zakaz_by_id(db, id))
        await message.answer(text="\nПользователь : "+id+
                             "\nАктивный заказ : "+zakaz_number+
                             "\nАдрес доставки: ",
                             reply_markup=problemkb)
        print(util.get_date(), 'Запрос баланса от ', str(message.from_user.id))
    else:
        pass



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start.start_info()
    sql.create_tables(db)
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
