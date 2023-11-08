import requests
import util

import os


def start_info():
    print('▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▉ ▊ ▉ ▉ ▊ ▉ ▊ ▉ ▊ ▊ ▋' +
                     '\n__________БОТ_ЗАГРУЗИЛСЯ_____________' +
                     '\n дата загрузки : ' + util.get_date() +
                     '\n__________ИНФО О СИСТЕМЕ_____________')

def get_server_ip():
    for li in os.popen('ipconfig /all'):
        print(li)



    ipurl = 'http://ipinfo.io/json'
    getIp = requests.get(ipurl)
    ip_list_srt = []
    for i in getIp.text.split(':'):
        ip_list_srt.append(i)
        ip_list = []
        for j in str(ip_list).split(','):
            ip_list.append(j)


def get_server_info():
    print('Информация о сервере : ')

    for lis in os.popen('systeminfo'):
        print(lis)
