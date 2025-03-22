import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

import inMemoryData

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
betek_chat_id = os.getenv('TELEGRAM_CHAT')

scheduler = AsyncIOScheduler()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply('Hello! I\'m a bot!')


async def send_simple_message():
    if not scheduler.running:
        logging.log(logging.INFO, 'Scheduler is not running')

    if len(inMemoryData.messageQueueData) != 0:
        message = inMemoryData.messageQueueData.pop(0)
        await bot.send_message(chat_id=betek_chat_id, text=message)


@dp.message(Command('discord'))
async def send_discord_online_members(message: types.Message):
    if len(inMemoryData.generalChannelData) == 0:
        await message.reply('No one is online')

    for channel, members in inMemoryData.generalChannelData.items():
        await message.reply(f'{channel}: {", ".join([member.display_name for member in members])}')


async def init() -> None:
    try:
        scheduler.start()
        await dp.start_polling(bot)
    except Exception as e:
        logging.log(logging.ERROR, e)


def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
    scheduler.add_job(send_simple_message, IntervalTrigger(seconds=15))
    loop.run_until_complete(init())
