import config
import datetime
import logging

def get_date():
    today = datetime.datetime.now()
    now = today.strftime("%Y-%m-%d %H:%M:%S")
    return str(now)

logging.basicConfig(level=logging.WARNING, filename=config.LOG_FILENAME,filemode="w")

def write_log(string):
    try:
        logging.info('\n'+str(get_date())+string)
    except:
        print('Ошибка записи в лог')


def write_bug(string):
    try:
        logging.warning('\n'+str(get_date())+string)
    except:
        print('Ошибка записи в лог')