import asyncio
import src.messages
import src.commands
# from src.bot import *
from src.chat_manager import *


async def main():
    me = await bot.get_me()
    print(me.username)

    # checker = asyncio.create_task(chat_checker())
    # await checker

    await bot.start()
    await bot.run_until_disconnected()

with bot:
    bot.loop.run_until_complete(main())
