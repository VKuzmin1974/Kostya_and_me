import locale
from datetime import *


def get_time():
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    current_date = date.today()
    current_time = datetime.now()
    current_day = current_date.day
    current_month = current_date.strftime('%B')
    current_year = current_date.year

    return (f"Сейчас {current_time.strftime('%H:%M:%S')}"
            f" {current_day} {current_month}"
            f" {current_year} года")
