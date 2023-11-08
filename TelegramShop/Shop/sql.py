import sqlite3
import asyncio
import config
import util

from sqlite3 import Error

def sql_start():
    try:
        global base #Объевление базы и курсора
        base = sqlite3.connect(config.LOTO_BASE_PATH)
        print('__________НАЙДЕНА БАЗА ДАННЫХ________\n loto.db STATUS : CONNECTED')
        return base
    except Error:
        print(Error)

def create_tables(base):
    try:
        print('__________СОЗДАН КУРСОР______________\n loto.db STATUS : OK')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS users
            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            TelegramId TEXT,
            UserName TEXT,
            Contact TEXT,
            Lang TEXT,  
            RegDate NUMERIC)''')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS catalog
            (catalog_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            GoodNumber INTEGER, 
            Price INTEGER)''')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS goods
            (good_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            GoodNumber INTEGER,
            GoodName TEXT, 
            PhotoUrl TEXT, 
            Description TEXT)''')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS zakaz
            (zakaz_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ZakazNumber INTEGER, 
            TelegramId TEXT,
            Cost INTEGER, 
            Description TEXT)''')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS busket
            (busket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusketNumber INTEGER, 
            TelegramId TEXT, 
            Cost INTEGER)''')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS busketgoods
            (busket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusketNumber INTEGER, 
            GoodNumber INTEGER, 
            Count INTEGER)''')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS addressbook
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
                              (telegarmId, usn, con, lan, regDate))
        print(regDate + ' Доб пользователем ' + telegarmId)
        base.commit()
    except:
        print('Ошибка добавления нового пользователя')

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

def add_test_goods(base):
    try:
        good_1 = 1000
        good_2 = 1001
        good_3 = 1002

        good_name_1 = 'Товар 1'
        good_name_2 = 'Товар 2'
        good_name_3 = 'Товар 3'

        path_1 = str(config.GOODS_IMG_PATH)+'1000.jpeg'
        path_2 = str(config.GOODS_IMG_PATH) + '1001.jpeg'
        path_3 = str(config.GOODS_IMG_PATH) + '1002.jpeg'

        desc_1 = 'Тест товар 1'
        desc_2 = 'Тест товар 2'
        desc_3 = 'Тест товар 3'

        base.cursor().execute('''INSERT INTO goods (GoodNumber, 
                              GoodName, 
                              PhotoUrl, 
                              Description)
                              ) VALUES (?, ?, ?, ?)''', (int(good_1), good_name_1, str(path_1), desc_1))
        base.cursor().execute('''INSERT INTO goods (GoodNumber, 
                                      GoodName, 
                                      PhotoUrl, 
                                      Description)
                                      ) VALUES (?, ?, ?, ?)''', (int(good_2), good_name_2, str(path_2), desc_2))
        base.cursor().execute('''INSERT INTO goods (GoodNumber, 
                                      GoodName, 
                                      PhotoUrl, 
                                      Description)
                                      ) VALUES (?, ?, ?, ?)''', (int(good_3), good_name_3, str(path_3), desc_3))
        base.commit()
    except Error:
        print(Error)


def get_zakaz_by_id(base, telegram_id):
    try:
        zakaz_result = base.cursor().execute("SELECT ZakazNumber FROM zakaz WHERE TelegramId = ?",
                                             [telegram_id]).fetchone()
        return zakaz_result
    except Error:
        print(Error)


