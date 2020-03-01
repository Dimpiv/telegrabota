import requests
import sqlite3
import time
import datetime
from datetime import timedelta


class ExApi:
    url = 'https://api.exchangeratesapi.io/'

    def __init__(self, base='USD'):
        self.base = base
        self.db = sqlite3.connect(":memory:")
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE rates
                          (currency text, rate float , last_date int)
                       """)
        self.db.commit()

    def get_rates(self, save: bool = True) -> dict:
        url = self.url + 'latest?base=' + self.base
        r = requests.get(url)
        result = r.json()
        if save:
            self.local_save(result.get('rates', dict()))
        return result.get('rates', dict())

    @staticmethod
    def get_timestamp() -> int:
        return int(round(time.time() * 1000))

    def local_save(self, rates: dict):
        date = self.get_timestamp()
        to_base = [(name, val, date) for name, val in rates.items()]
        self.cursor.executemany("INSERT INTO rates VALUES (?,?,?)", to_base)
        self.db.commit()

    def local_rates(self) -> dict:
        loc_data = self.cursor.execute(""" SELECT currency, rate FROM rates""").fetchall()
        result = {val[0]: val[1] for val in loc_data}
        return result

    def check_time(self, minutes: int = 1) -> bool:
        loc_time = self.cursor.execute(""" SELECT last_date FROM rates""").fetchone()
        now_time = self.get_timestamp()
        if now_time - loc_time[0] >= minutes * 60 * 1000:
            result = True
        else:
            result = False
        return result

    def convert_usd_to_cad(self, val: int = 1) -> float:
        sql = """ SELECT rate FROM rates WHERE currency=?"""

        self.cursor.execute(sql, ['USD'])
        c_1 = self.cursor.fetchone()[0]
        self.cursor.execute(sql, ['CAD'])
        c_2 = self.cursor.fetchone()[0]
        return round(val * c_1 * c_2, 2)

    def convert(self, base_cur: str = 'USD', convert_cur: str = 'CAD', val: int = 1):
        # TODO end to full convert functional
        pass

    def get_statistic(self, delay_time: int = 7) -> dict:
        start = datetime.datetime.now() - timedelta(days=delay_time)
        end = datetime.datetime.now()
        pre_string = f'history?start_at={start.strftime("%Y-%m-%d")}&end_at={end.strftime("%Y-%m-%d")}&base=USD&symbols=CAD'
        url = self.url + pre_string
        r = requests.get(url)
        result = r.json()
        return result
