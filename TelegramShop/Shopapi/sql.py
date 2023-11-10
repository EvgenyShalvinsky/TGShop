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
        util.time("Не найден файл ДБ shop.dll ")



def put_good_in_busket(base, tgid, good_number):
    user_in_busket = base.cursor().execute(
        '''SELECT COUNT(BusketNumber) FROM busket WHERE TelegramId = ?''',
        [tgid]
    ).fetchone()[0]
    good_in_basket = int(base.cursor().execute(
        '''SELECT COUNT(GoodNumber) FROM busketgoods WHERE BusketNumber = ?''',
        [tgid]
    ).fetchone()[0])
    try:
        if user_in_busket == 0:
            base.cursor().execute(
                '''INSERT INTO busketgoods (BusketNumber, GoodNumber, Count) VALUES (?, ?, ?)''',
                (tgid, good_number, 1)
            )
            base.cursor().execute(
                '''INSERT INTO busket (BusketNumber, TelegramId) VALUES (?, ?, ?)''',
                (tgid, tgid)
            )
        else:
            if good_in_basket == 0:
                base.cursor().execute(
                    '''INSERT INTO busketgoods (BusketNumber, GoodNumber, Count) VALUES (?, ?, ?)''',
                    (tgid, good_number, 1)
                )
            else:
                good_in_basket = int(good_in_basket)+1
                base.cursor().execute(
                    '''INSERT INTO busketgoods (BusketNumber, GoodNumber, Count) VALUES (?, ?, ?)''',
                    (tgid, good_number, good_in_basket)
                )


        base.commit()
    except Error:
        print(Error)
        print(str(util.get_date()) + ' Ошибка получения списка url фотографий товаров')



