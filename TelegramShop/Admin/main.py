import util
import sql
import asyncio
import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, message, LabeledPrice, PreCheckoutQuery, ContentTypes
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Объект бота
bot = Bot(token=config.TG_TOKEN)

#loop = asyncio.get_event_loop()
storage = MemoryStorage()

# Диспетчер
dp = Dispatcher(bot, storage=storage)
db = sql.connect()

class Good (StatesGroup):
    goodNumber = State()
    goodName = State()
    price = State()
    description = State()


class Id (StatesGroup):
    ids = State()

# Хэндлер на команду /start
@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await bot.send_message(731620137, text='Пользователь : '+str(message.from_user.id)+' подключился')
    sql.add_adm(
        db,
        str(message.from_user.id),
        str(message.from_user.username),
        str(message.from_user.first_name)+str(message.from_user.last_name),
        'Admin', util.time()
    )
    print('Команда старт от', str(message.from_user.id))
    await message.answer('\n/add - добавить ')

@dp.message_handler(commands=['del'])
async def cmd_start(message: types.Message):
    if message.get_args():
        goodNumber = int(message.get_args())
        sql.del_good(db, goodNumber)
    await bot.send_message(731620137, text='Пользователь : '+str(message.from_user.id)+' подключился')
    print('Команда del '+str(goodNumber)+' от'+str(message.from_user.id))
    await message.answer('\n/add - добавить ')

@dp.message_handler(commands=['add'])
async def cmd_add(message: types.Message):
    await bot.send_message(message.from_user.id, text='Введите номер продукта :')
    await Good.goodNumber.set()

async def get_good_number(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    goodNumber = message.text
    await state.update_data(goodNumber=goodNumber)
    await bot.send_message(user_id, text='Введите название : ')
    await Good.next()

async def get_good_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    goodName = message.text
    await state.update_data(goodName=goodName)
    await bot.send_message(user_id, text='Введите цену : ')
    await Good.next()

async def get_price(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    price = message.text
    await state.update_data(price=price)
    await bot.send_message(user_id, text='Введите описание : ')
    await Good.next()

async def get_description(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    description = message.text
    await state.update_data(description=description)
    good_dict = await state.get_data()
    sql.update_goods(
        db,
        int(good_dict['goodNumber']),
        good_dict['goodName'],
        str(config.GOODS_IMG_PATH)+str(good_dict['goodNumber'])+'.jpeg',
        good_dict['description']
    )
    sql.update_catalog(
        db,
        int(good_dict['goodNumber']),
        int(good_dict['price'])
    )
    await bot.send_message(user_id, text='Добавлен новый товар '+str(good_dict['goodName']))
    await state.finish()




dp.register_message_handler(get_good_number, state=Good.goodNumber)
dp.register_message_handler(get_good_name, state=Good.goodName)
dp.register_message_handler(get_price, state=Good.price)
dp.register_message_handler(get_description, state=Good.description)

#Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

    # Главная функция действия при старте
if __name__ == '__main__':
    util.start()
    sql.create_tables(db)
    asyncio.run(main())
