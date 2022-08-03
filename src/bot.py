import logging
from config import *
from telethon import TelegramClient

# logging.basicConfig(filename='info_logs.txt', encoding='utf-8', level=logging.INFO)
logging.basicConfig(filename='all_logs.txt', encoding='utf-8', level=logging.INFO)
bot = TelegramClient(bot_name, api_id, api_hash).start(bot_token=bot_token)
