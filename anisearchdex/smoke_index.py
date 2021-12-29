import time

from anisearchdex import sheet_service, LOGGER
from anisearchdex.config import SMOKE_SHEET_ID, SMOKE_SHEET_URL, NULL_MSG, SMOKE_INDEX_NAME
from anisearchdex.utils import cleaner, getSheetRange


def smoke_bytitle(query, whichTab):
    final_results = []
    RANGE = getSheetRange('smoke', whichTab)
    sheet_result = sheet_service.values().get(spreadsheetId=SMOKE_SHEET_ID, range=RANGE).execute().get('values', [])

    for i in sheet_result:
        if len(i) != 0:
            try:
                if query.lower() in i[0].lower() or query.lower() in i[1].lower():
                    title, alt_title, best_rel, alt_rel, reso, dual_audio, ss_comp, notes = genList(i)
                    result = [title, alt_title, best_rel, alt_rel, reso, dual_audio, ss_comp, notes]
                    final_results.append(result)
            except IndexError:
                # LOGGER.error(f"smoke-bytitle: {i}")
                pass

    return final_results, int(time.time())


def smoke_bytag(query, whichTab):
    final_results = []
    RANGE = getSheetRange('smoke', whichTab)
    sheet_result = sheet_service.values().get(spreadsheetId=SMOKE_SHEET_ID, range=RANGE).execute().get('values', [])

    for i in sheet_result:
        if len(i) != 0:
            try:
                if query.lower() in i[2].lower() or query.lower() in i[3].lower():
                    title, alt_title, best_rel, alt_rel, reso, dual_audio, ss_comp, notes = genList(i)
                    result = [title, alt_title, best_rel, alt_rel, reso, dual_audio, ss_comp, notes]
                    final_results.append(result)
            except IndexError:
                # LOGGER.error(f"smoke-bytag: {i}")
                pass

    return final_results, int(time.time())


def genList(i):
    try:
        title = cleaner([i][0][0])
    except IndexError:
        title = NULL_MSG
    try:
        alt_title = cleaner([i][0][1])
    except IndexError:
        alt_title = NULL_MSG
    try:
        best_rel = cleaner([i][0][2])
    except IndexError:
        best_rel = NULL_MSG
    try:
        alt_rel = cleaner([i][0][3])
    except IndexError:
        alt_rel = NULL_MSG
    try:
        reso = cleaner([i][0][4])
    except IndexError:
        reso = NULL_MSG
    try:
        dual_audio = cleaner([i][0][5])
    except IndexError:
        dual_audio = NULL_MSG
    try:
        notes = [i][0][6]
    except IndexError:
        notes = NULL_MSG
    try:
        ss_comp = [i][0][7]
    except IndexError:
        ss_comp = NULL_MSG

    return title, alt_title, best_rel, alt_rel, reso, dual_audio, ss_comp, notes


def gen_smoke_msg(input_list):
    msg = f'''
<b>Bloat Release Finder 🔎</b>

<b>Title</b>
{input_list[0]}

<b>Alternative Title</b>
{input_list[1]}

<b>Best Release</b>
{input_list[2]}

<b>Alternate Release</b>
{input_list[3]}

<b>Resolution</b>
{input_list[4]}

<b>Dual Audio</b>
{input_list[5]}

<b>Comparisons</b>
{input_list[6]}

<b>Notes</b>
{input_list[7]}

<b>Powered by </b><a href="{SMOKE_SHEET_URL}">{SMOKE_INDEX_NAME}</a>
'''
    return msg
