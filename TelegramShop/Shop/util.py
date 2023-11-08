import datetime
import logging

def get_date():
    today = datetime.datetime.now()
    now = today.strftime("%Y-%m-%d %H:%M:%S")
    return now
