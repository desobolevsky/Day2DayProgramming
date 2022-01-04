# Onliner Prices Monitor
This script parses data from onliner.by online shop and notifies user via Telegram about price changes.
I've coded it mostly to track prices on videocards in my hometown, Minsk, Belarus. (xDDD)
## Tech
This script uses following technologies:
 - BeautifulSoup4 - for HTML pages parsing
 - sqlite3 - lightweight database
 - Telegram Web Api - for user notification via Telegram Messanger
## Installation and usage
 Clone project
```sh
git clone https://github.com/desobolevsky/BYCurrenciesTelegramBot.git
```
Create virtual environment
```shell
python3 -m venv .venv
source .venv/bin/activate
```
Install requirements
```shell
pip install -r requirements.txt
```
Create sqlite3 database
```shell
sqlite3 DB.db < init.sql 
```
Add links to onliner.by for goods you're interested in in some file, e.g. goods.txt

Create and fill .env file
```shell
cat .env_example > .env
```
Variables:
- DB_FILENAME - sqlite3 database filename
- GOODS_FILENAME - name of the file with links to goods
- TIME_DELAY_SECONDS - job time delay between updates
- TELEGRAM_BOT_TOKEN - token for your telegram bot
- TELEGRAM_CHAT_ID - id of chat where notifications should be sent

Run script
```shell
python3 main.py
```
