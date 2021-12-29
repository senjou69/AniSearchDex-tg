import time

from anisearchdex import sheet_service
from anisearchdex.config import FANSUB_SHEET_ID, FANSUB_SHEET_URL, NULL_MSG, FANSUB_INDEX_NAME
from anisearchdex.utils import cleaner, getSheetRange


def fansub_bytitle(query, whichTab):
    final_results = []
    RANGE = getSheetRange('fansub', whichTab)
    sheet_result = sheet_service.values().get(spreadsheetId=FANSUB_SHEET_ID, range=RANGE).execute().get('values', [])

    for i in sheet_result:
        if len(i) != 0:
            try:
                if query.lower() in i[5].lower() or query.lower() in i[0].lower():
                    title, alt_title, best_rel, alt_rel, reso, notes, sorting = genList(i)
                    result = [title, alt_title, best_rel, alt_rel, reso, notes, sorting]
                    final_results.append(result)
            except IndexError:
                # LOGGER.error(f"fansub-bytitle: {i}")
                pass

    return final_results, int(time.time())


def fansub_bytag(query, whichTab):
    final_results = []
    RANGE = getSheetRange('fansub', whichTab)
    sheet_result = sheet_service.values().get(spreadsheetId=FANSUB_SHEET_ID, range=RANGE).execute().get('values', [])

    for i in sheet_result:
        if len(i) != 0:
            try:
                if query.lower() in i[1].lower() or query.lower() in i[2].lower():
                    title, alt_title, best_rel, alt_rel, reso, notes, sorting = genList(i)
                    result = [title, alt_title, best_rel, alt_rel, reso, notes, sorting]
                    final_results.append(result)
            except IndexError:
                # LOGGER.error(f"fansub-bytag: {i}")
                pass

    return final_results, int(time.time())


def genList(i):
    try:
        title = cleaner([i][0][0])
    except IndexError:
        title = NULL_MSG
    try:
        alt_title = cleaner([i][0][5])
    except IndexError:
        alt_title = NULL_MSG
    try:
        best_rel = cleaner([i][0][1])
    except IndexError:
        best_rel = NULL_MSG
    try:
        alt_rel = cleaner([i][0][2])
    except IndexError:
        alt_rel = NULL_MSG
    try:
        reso = cleaner([i][0][3])
    except IndexError:
        reso = NULL_MSG
    try:
        notes = cleaner([i][0][4])
    except IndexError:
        notes = NULL_MSG
    try:
        sorting = cleaner([i][0][6])
    except IndexError:
        sorting = NULL_MSG
    return title, alt_title, best_rel, alt_rel, reso, notes, sorting


def gen_fansub_msg(list_data):
    text = f'''
<b>Bloat Release Finder 🔎</b>

<b>Title</b>
{list_data[0]}

<b>Alternate Title</b>
{list_data[1]}

<b>Best Release</b>
{list_data[2]}

<b>Alternate Release</b>
{list_data[3]}

<b>Resolution</b>
{list_data[4]}

<b>Notes</b>
{list_data[5]}

<b>Sorting Key</b>
{list_data[6]}

<b>Powered by </b><a href="{FANSUB_SHEET_URL}">{FANSUB_INDEX_NAME}</a>
'''
    return text
