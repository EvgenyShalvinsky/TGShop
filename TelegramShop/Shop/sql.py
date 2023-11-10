import sqlite3
import asyncio
import config
import util


from sqlite3 import Error

def connect():
    try:
        global base
        base = sqlite3.connect(config.BASE_PATH)
        util.write_log(" Найден файл ДБ shop.dll ")
        return base
    except:
        util.write_bug("Не найден файл ДБ shop.dll ")

def create_tables(base):
    try:
        print('__________СОЗДАН КУРСОР______________\n loto.db STATUS : OK')
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS users
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            TelegramId TEXT,
            UserName TEXT,
            Contact TEXT,
            Lang TEXT,  
            RegDate NUMERIC)''')
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS catalog
            (catalog_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            GoodNumber INTEGER, 
            Price INTEGER)''')
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS goods
            (good_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            GoodNumber INTEGER,
            GoodName TEXT, 
            PhotoUrl TEXT, 
            Description TEXT)''')
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS zakaz
            (zakaz_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ZakazNumber INTEGER, 
            TelegramId TEXT,
            Cost INTEGER, 
            Description TEXT)''')
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS busket
            (busket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusketNumber INTEGER, 
            TelegramId TEXT, 
            Cost INTEGER)''')
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS busketgoods
            (busket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusketNumber INTEGER, 
            GoodNumber INTEGER,
            Count INTEGER)''')
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS addressbook
            (address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            TelegramId TEXT,
            City TEXT, 
            Street TEXT,
            Build_number TEXT, 
            Flat_number TEXT)''')
        base.commit()
    except Error:
        print(Error)
        print(str(util.get_date())+' Ошибка создания таблиц')

def get_good_number(base):
    try:
        good_number = base.cursor().execute('''SELECT GoodNumber FROM goods''').fetchall()
        return list(good_number)
    except Error:
        print(Error)
        print(str(util.get_date()) + ' Ошибка получения списка url фотографий товаров')


#Добавление нового игрока в БД
def get_photos_url(base):
    try:
        photos_url = base.cursor().execute('''SELECT PhotoUrl FROM goods''').fetchall()
        return photos_url
    except Error:
        print(Error)
        print(str(util.get_date()) + ' Ошибка получения списка url фотографий товаров')

def get_good_name(base):
    try:
        good_name = base.cursor().execute('''SELECT GoodName FROM goods''').fetchall()
        return list(good_name)
    except Error:
        print(Error)
        print(str(util.get_date()) + ' Ошибка получения списка url фотографий товаров')


def add_user(base, telegarmId, usn, con, lan, regDate):
    try:
        base.cursor().execute('''INSERT INTO users (TelegramId, UserName, Contact, Lang, RegDate) VALUES (?, ?)''',
                              (str(telegarmId), str(usn), str(con), str(lan), regDate))
        util.write_log(' Доб пользователем ' + str(telegarmId))
        base.commit()
    except:
        util.write_bug('Ошибка добавления нового пользователя')

def get_name_by_number(base, number):
    try:
        name = base.cursor().execute('''SELECT GoodName FROM goods WHERE GoodNumber = ?''', [number]).fetchone()
        return name[0]
    except:
        print('\n'+str(util.get_date())+' Ошибка в запросе ')

def get_price_by_number(base, number):
    try:
        price = base.cursor().execute('''SELECT Price FROM catalog WHERE GoodNumber = ?''', [number]).fetchone()
        return price[0]
    except:
        print('\n'+str(util.get_date())+' Ошибка в запросе ')

def get_by_number_name(base, name):
    try:
        name = str(name)
        number = base.cursor().execute('''SELECT GoodNumber FROM goods WHERE GoodName = ?''', [name]).fetchone()
        return number[0]
    except:
        print('\n'+str(util.get_date())+' Ошибка в запросе ')

def get_decs_by_number(base, num):
    try:
        desc = base.cursor().execute('''SELECT Description FROM goods WHERE GoodNumber = ?''', [num]).fetchone()
        return desc[0]
    except:
        print('\n'+str(util.get_date())+' Ошибка в запросе ')

def is_busket(base, tgid):
    user_in_busket = base.cursor().execute(
        '''SELECT COUNT(BusketNumber) FROM busket WHERE TelegramId = ?''',
        [tgid]
    ).fetchone()[0]
    return user_in_busket

def put_good_in_busket(base, tgid, good_number):
    user_in_busket = base.cursor().execute(
        '''SELECT COUNT(BusketNumber) FROM busket WHERE TelegramId = ?''',
        [tgid]
    ).fetchone()[0]
    print(user_in_busket)
    print(type(user_in_busket))
    good_in_basket = int(base.cursor().execute(
        '''SELECT COUNT(GoodNumber) FROM busketgoods WHERE BusketNumber = ?''',
        [tgid]
    ).fetchone()[0])
    print(good_in_basket)
    print(type(good_in_basket))
    try:
        if user_in_busket == 0:
            try:
                base.cursor().execute(
                    '''INSERT INTO busketgoods (BusketNumber, GoodNumber, Count) VALUES (?, ?, ?)''',
                    (int(tgid), good_number, 1)
                )
            except Error:
                print(Error)
                print('тут 150')
            try:
                base.cursor().execute(
                    '''INSERT INTO busket (BusketNumber, TelegramId) VALUES (?, ?)''',
                    (int(tgid), tgid)
                )
            except Error:
                print(Error)
                print('тут 161')
        else:
            if good_in_basket == 0:
                base.cursor().execute(
                    '''INSERT INTO busketgoods (BusketNumber, GoodNumber, Count) VALUES (?, ?, ?)''',
                    (int(tgid), good_number, 1)
                )
            else:
                good_in_basket = int(good_in_basket)+1
                base.cursor().execute(
                    '''DELETE FROM busketgoods WHERE BusketNumber = ? AND GoodNumber = ?''',
                    [int(tgid), good_number]
                )
                base.cursor().execute(
                    '''INSERT INTO busketgoods (BusketNumber, GoodNumber, Count) VALUES (?, ?, ?)''',
                    (int(tgid), good_number, good_in_basket)
                )
        base.commit()
    except Error:
        print(Error)
        print(str(util.get_date()) + ' Ошибка получения списка url фотографий товаров')



def get_zakaz_by_id(base, telegram_id):
    try:
        zakaz_result = base.cursor().execute("SELECT ZakazNumber FROM zakaz WHERE TelegramId = ?",
                                             [telegram_id]).fetchone()
        return zakaz_result
    except Error:
        print(Error)



def get_goodnum_by_user(base, tgid):
    try:
        goods_in_busket = base.cursor().execute(
            '''SELECT GoodNumber FROM busketgoods WHERE BusketNumber = ?''',
            [int(tgid)]
        ).fetchall()
        return list(goods_in_busket)
    except:
        util.write_bug(str(Error.__str__())+" Не получен номер товара из корзины ")


def get_count_goods_in_busket(base, num):
    try:
        count_good = base.cursor().execute(
            '''SELECT Count FROM busketgoods WHERE GoodNumber = ?''',
            [int(num)]
        ).fetchone()[0]
        return str(count_good)
    except:
        util.write_bug(str(Error.__str__()) + " Не получено кол-во товара из корзины ")