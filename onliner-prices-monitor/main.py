import os
import sqlite3
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv('.env')

DB_FILENAME = os.environ.get('DB_FILENAME', 'database.db')
GOODS_FILENAME = os.environ.get('GOODS_FILENAME', 'goods.txt')
TIME_DELAY_SECONDS = int(os.environ.get('TIME_DELAY_SECONDS', 3600))
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

PRICE_CHANGE_MESSAGE = '{good_url}\nЦена изменилась с {old_price} на {new_price}. Разница: {change}'


def import_goods_to_db(filename, db_con, db_cursor) -> None:
    with open(filename, 'r') as file:
        goods = [line.rstrip() for line in file]
    db_cursor.executemany(
        '''INSERT OR IGNORE INTO goods (url) VALUES (?)''',
        [(good,) for good in goods]
    )
    db_con.commit()


def get_db_goods(db_cursor) -> List[str]:
    query = db_cursor.execute('''SELECT id, url FROM goods''')
    return query.fetchall()


def get_good_price(url: str) -> float:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content)
    price_tag = soup.findAll('a', {'class': "offers-description__link offers-description__link_nodecor"})
    # if good isn't present at stores or outdated return 0
    if not price_tag:
        return 0
    price = float(price_tag[0].text.strip()[:-3].replace(' ', '').replace(',', '.'))
    return price


def notify(message: str) -> None:
    response = requests.post(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
        data={'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    )
    response.raise_for_status()


def run():
    db_con = sqlite3.connect(DB_FILENAME)
    db_cursor = db_con.cursor()
    import_goods_to_db(GOODS_FILENAME, db_con, db_cursor)
    goods = get_db_goods(db_cursor)

    notify('The script has started.')
    while True:
        for good in goods:
            good_id, good_url = good
            try:
                print(f'Getting price of good {good_url}')
                good_price = get_good_price(good_url)
                query_result = db_cursor.execute(
                    f'''SELECT price FROM price WHERE good_id=:good_id ORDER BY TIMESTAMP DESC''',
                    {'good_id': good_id}
                )
                last_update_good = query_result.fetchall()
                if last_update_good:
                    last_update_price = last_update_good[0][0]
                    if good_price != last_update_price:
                        db_cursor.execute(
                            f'''INSERT INTO price (good_id, price, timestamp) VALUES (?, ?, ?)''',
                            (good_id, good_price, int(time.time()))
                        )
                        price_change_msg = PRICE_CHANGE_MESSAGE.format(good_url=good_url,
                                                                       old_price=last_update_price,
                                                                       new_price=good_price,
                                                                       change=abs(last_update_price - good_price))
                        notify(price_change_msg)
                else:
                    db_cursor.execute(
                        f'''INSERT INTO price (good_id, price, timestamp) VALUES (?, ?, ?)''',
                        (good_id, good_price, int(time.time()))
                    )
            except requests.exceptions.RequestException as ex:
                print(f'Error on request on good {good_url}. Exception: {ex}')

        db_con.commit()
        time.sleep(TIME_DELAY_SECONDS)


if __name__ == '__main__':
    run()
