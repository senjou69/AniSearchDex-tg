import time

from aiogram import executor
from aiogram.types import Message
from humanfriendly import format_timespan
from anisearchdex import dp, bot, LOGGER, botStartTime
from anisearchdex.config import HELP_TEXT, USERNAME, WELCOME_MSG, SEARCH_MSG, OWNER_ID, LOG_FILE_NAME, CMD_TIMEOUT
from anisearchdex.pagination import genIndKeyboard, genExpIndBtn, genDelBtn
from anisearchdex.stats_sheet import gen_sheet_stats
from anisearchdex.utils import checkQuery, extractQuery


async def handler_throttled(message: Message, **kwargs):
    LOGGER.warning(f"User @{message.from_user.username} ({message.from_user.id}) is spamming {message.text}")


@dp.message_handler(commands=['start', f"start@{USERNAME}"])
@dp.throttled(rate=CMD_TIMEOUT, on_throttled=handler_throttled)
async def start(message: Message):
    await message.reply(WELCOME_MSG)


@dp.message_handler(commands=['series', f"series@{USERNAME}"])
async def series(message: Message):
    query = extractQuery(message)
    if checkQuery(query) is True:
        await message.reply(SEARCH_MSG.format(query), reply_markup=genIndKeyboard('series'))
    else:
        await message.reply(checkQuery(query))


@dp.message_handler(commands=['movies', f"movies@{USERNAME}"])
async def movies(message: Message):
    query = extractQuery(message)
    if checkQuery(query) is True:
        await message.reply(SEARCH_MSG.format(query), reply_markup=genIndKeyboard('movies'))
    else:
        await message.reply(checkQuery(query))


@dp.message_handler(commands=['expose', f"expose@{USERNAME}"])
async def bytag(message: Message):
    query = extractQuery(message)
    if checkQuery(query) is True:
        await message.reply(SEARCH_MSG.format(query), reply_markup=genExpIndBtn())
    else:
        await message.reply(checkQuery(query))


@dp.message_handler(commands=['stats', f"stats@{USERNAME}"])
@dp.throttled(rate=CMD_TIMEOUT, on_throttled=handler_throttled)
async def sheet_stats(message: Message):
    hold_on = await message.reply(text="<b>Hold on!</b>")
    text = gen_sheet_stats()
    await hold_on.edit_text(text=text,
                            reply_markup=genDelBtn(),
                            disable_web_page_preview=True)


@dp.message_handler(commands=['help', f"help@{USERNAME}"])
@dp.throttled(rate=CMD_TIMEOUT, on_throttled=handler_throttled)
async def halp(message: Message):
    await message.reply(text=HELP_TEXT,
                        reply_markup=genDelBtn(),
                        disable_web_page_preview=True)


@dp.message_handler(commands=['up', f"up@{USERNAME}"])
@dp.throttled(rate=CMD_TIMEOUT, on_throttled=handler_throttled)
async def uptime(message: Message):
    await message.reply(text="<b>I haven't slept for</b> {}".format(format_timespan(time.time()-botStartTime)),
                        reply_markup=genDelBtn(),
                        disable_web_page_preview=True)


@dp.message_handler(commands=['log'])
async def sendlog(message: Message):
    if message.chat.id == OWNER_ID and message.chat.type == 'private':
        with open(LOG_FILE_NAME, 'rb') as file:
            await bot.send_document(message.chat.id, file)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
