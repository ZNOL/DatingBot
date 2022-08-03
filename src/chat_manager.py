import asyncio
from src.bot import *
from src.users import *
from src.database import *
from datetime import datetime
from telethon.tl.types import TypeChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import AddChatUserRequest  # delete?
from telethon.tl.functions.channels import InviteToChannelRequest


async def user_delete_from_chat(user_id):
    await bot(EditBannedRequest(chat_id, user_id, TypeChatBannedRights(
        until_date=None,
        view_messages=True,
    )))


async def user_add_to_chat(user_id):
    await bot(EditBannedRequest(chat_id, user_id, TypeChatBannedRights(
        until_date=None,
        view_messages=None,
    )))


async def chat_checker():
    while True:
        today = datetime.now()

        chat_participants = set()
        try:
            participants = await bot.get_participants(chat_id)
            for user in participants:
                chat_participants.add(user.id)
        except Exception as e:
            logging.error(str(e))

        users = chat_participants.union(users_list)
        for user_id in users:
            try:
                if user_id in users_list:
                    user_time = get_subscription(user_id)
                else:
                    user_time = None

                if user_time is None or user_time < today:
                    await user_delete_from_chat(user_id)
                    logging.info(f'User: {user_id} deleted')
                else:
                    await user_add_to_chat(user_id)
                    logging.info(f'User: {user_id} added')
            except Exception as e:
                logging.error(f'User: {user_id} | {e}')

        logging.info('Chat updated')
        await asyncio.sleep(60)
