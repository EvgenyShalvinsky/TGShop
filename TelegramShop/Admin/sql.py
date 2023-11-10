import sqlite3
import config
import util


def connect():
    try:
        global base
        base = sqlite3.connect(config.BASE_PATH)
        util.write_log(" Найден файл ДБ shop.dll ")
        return base
    except:
        util.time("Не найден файл ДБ shop.dll ")



def create_tables(base):
    try:
        con = base.cursor()
        con.execute('''CREATE TABLE IF NOT EXISTS users
                           (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           TgId TEXT,
                           Name TEXT,
                           UserName TEXT,
                           Role TEXT,
                           RegDate NUMERIC
                           )'''
                    )
        base.commit()
        util.write_log("Создана таблица users")
    except:
        util.write_bug("Ошибка создания Таблиц")

def add_adm(base, id, name, username, role, date):
    try:
        base.cursor().execute(
            '''INSERT INTO adm(TgId, Name, UserName, Role, RegDate) VALUES (?,?,?,?,?)''',
            (id, name, username, role, date)
        )
        base.commit()
        util.write_log("Добавлен администратор")
    except:
        util.write_bug("Ошибка добавления администратора")

def update_goods(base, num, name, url, descr):
    try:
        base.cursor().execute(
            '''INSERT INTO goods(GoodNumber, GoodName, PhotoUrl, Description) VALUES (?,?,?,?)''',
            (num, name, url, descr)
        )
        base.commit()
        util.write_log("Добавлен администратор")
    except:
        util.write_bug("Ошибка добавления администратора")

def update_catalog(base, num, price):
    try:
        base.cursor().execute(
            '''INSERT INTO catalog(GoodNumber, Price) VALUES (?,?)''',
            (num, price)
        )
        base.commit()
        util.write_log("Добавлен администратор")
    except:
        util.write_bug("Ошибка добавления администратора")

def del_good(base, num):
    try:
        base.cursor().execute(
            '''DELETE FROM catalog WHERE GoodNumber = ?''',
            [num]
        )
        base.commit()
        util.write_log("Товар "+str(num)+' удален')
    except:
        util.write_bug("Товар " + str(num) + ' не может быть удален')
