import datetime
import logging
import config
def time():
    time = datetime.datetime.now()
    return time

def start():
    print('▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▉ ▊ ▉ ▉ ▊ ▉ ▊ ▉ ▊ ▊ ▊ ▋' +
          '\n__________БОТ_ЗАГРУЗИЛСЯ_____________' +
          '\n дата загрузки : ' + str(time()))

logging.basicConfig(level=logging.WARNING, filename=config.LOG_FILENAME,filemode="w")

def write_log(string):
    try:
        logging.info('\n'+str(time())+string)
    except:
        print('Ошибка записи в лог')


def write_bug(string):
    try:
        logging.warning('\n'+str(time())+string)
    except:
        print('Ошибка записи в лог')