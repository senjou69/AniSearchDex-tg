import time

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified, MessageToEditNotFound

from anisearchdex import bot, dp, message_info, callback_lock
from anisearchdex.certain_index import gen_fansub_msg, fansub_bytag, fansub_bytitle
from anisearchdex.config import INTRUDER_MSG, SEARCH_MSG, NO_PAGE_MSG, NO_RESULT_MSG, TRASH_EMOJI
from anisearchdex.smoke_index import gen_smoke_msg, smoke_bytag, smoke_bytitle
from anisearchdex.utils import isSessionValid, extractQuery, cache_clear


def genNavBtn(current_page, total_result):
    if current_page == 1 and total_result > 1:
        return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton("Prev", callback_data=f'nogoing'),
            InlineKeyboardButton(f"{current_page}/{total_result}", callback_data=f'null'),
            InlineKeyboardButton("Next", callback_data=f'next')
        ).add(InlineKeyboardButton("Go back", callback_data=f'back')
              ).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))
    elif total_result == 1:
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(f"{current_page}/{total_result}", callback_data=f'null')
        ).add(InlineKeyboardButton("Go back", callback_data=f'back')
              ).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))
    elif (total_result != 0 or current_page != 0) and (total_result == current_page):
        return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton("Prev", callback_data=f'prev'),
            InlineKeyboardButton(f"{current_page}/{total_result}", callback_data=f'null'),
            InlineKeyboardButton("Next", callback_data=f'nogoing')
        ).add(InlineKeyboardButton("Go back", callback_data=f'back')
              ).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))
    elif current_page != 1 and total_result > 1:
        return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton("Prev", callback_data=f'prev'),
            InlineKeyboardButton(f"{current_page}/{total_result}", callback_data=f'null'),
            InlineKeyboardButton("Next", callback_data=f'next')
        ).add(InlineKeyboardButton("Go back", callback_data=f'back')
              ).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))
    elif total_result > 1:
        return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton("Prev", callback_data=f'prev'),
            InlineKeyboardButton(f"{current_page}/{total_result}", callback_data=f'null'),
            InlineKeyboardButton("Next", callback_data=f'nogoing')
        ).add(InlineKeyboardButton("Go back", callback_data=f'back')
              ).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))
    else:
        return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(f"Error", callback_data=f'null')
        ).add(InlineKeyboardButton("Go back", callback_data=f'back')
              ).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))


def genIndKeyboard(whichtype):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton("Smoke Index", callback_data=f'smoke_{whichtype}'),
        InlineKeyboardButton("Fansub Index", callback_data=f'fansub_{whichtype}')
    )


def genExpIndBtn():
    return InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Smoke (series)", callback_data=f'exp_smok_ser'),
                                                 InlineKeyboardButton("Fansubber (series)",
                                                                      callback_data=f'exp_fans_ser'),
                                                 InlineKeyboardButton("Smoke (movies)", callback_data=f'exp_smok_mov'),
                                                 InlineKeyboardButton("Fansubber (movies)",
                                                                      callback_data=f'exp_fans_mov')
                                                 )


def genDelBtn():
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))


def genExpiredBtn():
    return InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton("Session Expired", callback_data=f'null')
                                                 ).add(InlineKeyboardButton(TRASH_EMOJI, callback_data=f'delete'))


# -----------
@dp.callback_query_handler(lambda c: c.data.startswith(('smoke_series', 'smoke_movies', 'fansub_series', 'fansub_movies', 'exp_smok_ser',
                                                        'exp_fans_ser', 'exp_smok_mov', 'exp_fans_mov')))
async def process_callback_data(call: CallbackQuery):
    message_indentifier = call.message.chat.id, call.message.message_id
    m_message = message_info.get(message_indentifier)
    if m_message:
        session_time = m_message[0]
        if isSessionValid(session_time) is False:
            return await call.message.edit_reply_markup(reply_markup=genExpiredBtn())
    else:
        if isSessionValid(call.message.date.timestamp()) is False:
            return await call.message.edit_reply_markup(reply_markup=genExpiredBtn())

    if call.from_user.id == call.message.reply_to_message.from_user.id:
        query = extractQuery(call.message.reply_to_message)
        if call.data == "smoke_series":
            await init_search(query, 'series', 'smoke', call.message)
        elif call.data == "smoke_movies":
            await init_search(query, 'movies', 'smoke', call.message)
        elif call.data == "fansub_series":
            await init_search(query, 'series', 'fansub', call.message)
        elif call.data == "fansub_movies":
            await init_search(query, 'movies', 'fansub', call.message)
        elif call.data == "exp_smok_ser":
            await init_search(query, 'series', 'e_smoke', call.message)
        elif call.data == "exp_smok_mov":
            await init_search(query, 'movies', 'e_smoke', call.message)
        elif call.data == "exp_fans_ser":
            await init_search(query, 'series', 'e_fansub', call.message)
        elif call.data == "exp_fans_mov":
            await init_search(query, 'movies', 'e_fansub', call.message)
        await call.answer()
    else:
        await bot.answer_callback_query(call.id, text=INTRUDER_MSG, show_alert=True)


@dp.callback_query_handler(lambda c: c.data.startswith(('prev', 'next', 'back', 'delete', 'nogoing', 'null')))
async def navBtnHandler(call: CallbackQuery):
    message_indentifier = call.message.chat.id, call.message.message_id
    m_message = message_info.get(message_indentifier)
    if m_message:
        session_time = m_message[0]
        query = m_message[4]
        whichtype = m_message[5]
        whichIndex = m_message[3]
        results = m_message[1]
        current_page = m_message[2]
    else:
        session_time = 0

    async with callback_lock:
        if call.data == 'delete' and call.from_user.id == call.message.reply_to_message.from_user.id:
            try:
                message_info.pop(message_indentifier)
            except KeyError:
                pass
            return await call.message.delete()
        elif isSessionValid(session_time) is True:
            if call.from_user.id == call.message.reply_to_message.from_user.id:
                session_time = int(time.time())
                if call.data == "next":
                    if current_page < len(results):
                        current_page += 1
                        current_index = current_page - 1
                        if whichIndex == 'smoke' or whichIndex == 'e_smoke':
                            text = gen_smoke_msg(results[current_index])
                        elif whichIndex == 'fansub' or whichIndex == 'e_fansub':
                            text = gen_fansub_msg(results[current_index])
                        await call.message.edit_text(
                            text=text,
                            reply_markup=genNavBtn(current_page, len(results)),
                            disable_web_page_preview=True)
                    message_info[message_indentifier] = session_time, results, current_page, whichIndex, query, whichtype
                elif call.data == "prev":
                    if current_page != 0:
                        current_page -= 1
                        current_index = current_page - 1
                        if whichIndex == 'smoke' or whichIndex == 'e_smoke':
                            text = gen_smoke_msg(results[current_index])
                        elif whichIndex == 'fansub' or whichIndex == 'e_fansub':
                            text = gen_fansub_msg(results[current_index])
                        await call.message.edit_text(
                            text=text,
                            reply_markup=genNavBtn(current_page, len(results)),
                            disable_web_page_preview=True)
                    message_info[message_indentifier] = session_time, results, current_page, whichIndex, query, whichtype
                elif call.data == 'back':
                    if whichIndex == 'e_smoke' or whichIndex == 'e_fansub':
                        await call.message.edit_text(text=SEARCH_MSG.format(query),
                                                reply_markup=genExpIndBtn())
                    elif whichtype == 'series':
                        await call.message.edit_text(text=SEARCH_MSG.format(query),
                                                reply_markup=genIndKeyboard('series'))
                    elif whichtype == 'movies':
                        await call.message.edit_text(text=SEARCH_MSG.format(query),
                                                reply_markup=genIndKeyboard('movies'))
                elif call.data == 'nogoing':
                    await call.answer(text=NO_PAGE_MSG,
                                      show_alert=True)
                elif call.data == 'null':
                    await call.answer()
            else:
                await call.answer(text=INTRUDER_MSG,
                                  show_alert=True)
        else:
            try:
                message_info.pop(message_indentifier)
            except KeyError:
                pass
            try:
                await call.message.edit_reply_markup(reply_markup=genExpiredBtn())
            except MessageNotModified:
                pass
            except MessageToEditNotFound:
                pass


async def init_search(query, whichtype, whichIndex, message):
    cache_clear()
    if whichtype == 'series':
        if whichIndex == 'smoke':
            results, session_time = smoke_bytitle(query, 'series')
        else:
            results, session_time = fansub_bytitle(query, 'series')

        if whichIndex == 'e_smoke':
            results, session_time = smoke_bytag(query, 'series')
        elif whichIndex == 'e_fansub':
            results, session_time = fansub_bytag(query, 'series')

    elif whichtype == 'movies':
        if whichIndex == 'smoke':
            results, session_time = smoke_bytitle(query, 'movies')
        else:
            results, session_time = fansub_bytitle(query, 'movies')

        if whichIndex == 'e_smoke':
            results, session_time = smoke_bytag(query, 'movies')
        elif whichIndex == 'e_fansub':
            results, session_time = fansub_bytag(query, 'movies')

    if len(results) == 0:
        reply = await message.edit_text(text=NO_RESULT_MSG,
                                        reply_markup=genDelBtn())
    else:
        if whichIndex == 'smoke' or whichIndex == 'e_smoke':
            reply = await message.edit_text(text=gen_smoke_msg(results[0]),
                                            reply_markup=genNavBtn(1, len(results)),
                                            disable_web_page_preview=True)

        elif whichIndex == 'fansub' or whichIndex == 'e_fansub':
            reply = await message.edit_text(text=gen_fansub_msg(results[0]),
                                            reply_markup=genNavBtn(1, len(results)),
                                            disable_web_page_preview=True)

    message_info[(reply.chat.id, reply.message_id)] = session_time, results, 1, whichIndex, query, whichtype
