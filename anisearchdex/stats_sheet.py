from anisearchdex import sheet_service, drive_service
from anisearchdex.config import FANSUB_SHEET_ID, SMOKE_SHEET_ID, SMOKE_SHEET_URL, FANSUB_INDEX_NAME, SMOKE_INDEX_NAME, \
    SMOKE_SERIES_STATS_RANGE, SMOKE_MOVIES_STATS_RANGE, FANSUB_SERIES_STATS_RANGE, FANSUB_MOVIES_STATS_RANGE
from anisearchdex.utils import parseIsoDate


def gen_sheet_stats():
    certain_total_series = len(sheet_service.values().get(spreadsheetId=FANSUB_SHEET_ID, range=FANSUB_SERIES_STATS_RANGE).execute().get('values', []))
    certain_total_movies = len(sheet_service.values().get(spreadsheetId=FANSUB_SHEET_ID, range=FANSUB_MOVIES_STATS_RANGE).execute().get('values', []))
    certain_drive_sheet = drive_service.files().get(fileId=FANSUB_SHEET_ID, fields='createdTime,modifiedTime,version').execute()

    smoke_total_series = len(sheet_service.values().get(spreadsheetId=SMOKE_SHEET_ID, range=SMOKE_SERIES_STATS_RANGE).execute().get('values', []))
    smoke_total_movies = len(sheet_service.values().get(spreadsheetId=SMOKE_SHEET_ID, range=SMOKE_MOVIES_STATS_RANGE).execute().get('values', []))
    smoke_drive_sheet = drive_service.files().get(fileId=SMOKE_SHEET_ID, fields='createdTime,modifiedTime,version').execute()

    certain_sheet_created_time = parseIsoDate(certain_drive_sheet.get('createdTime'))
    certain_sheet_modified_time = parseIsoDate(certain_drive_sheet.get('modifiedTime'))
    certain_sheet_version = certain_drive_sheet.get('version')

    smoke_sheet_created_time = parseIsoDate(smoke_drive_sheet.get('createdTime'))
    smoke_sheet_modified_time = parseIsoDate(smoke_drive_sheet.get('modifiedTime'))
    smoke_sheet_version = smoke_drive_sheet.get('version')

    return f"""<b>Stats of</b> <a href="{SMOKE_SHEET_URL}">{FANSUB_INDEX_NAME}</a>

<code><b>Series              :</b> <code>{certain_total_series}</code>
<b>Movies              :</b> <code>{certain_total_movies}</code>
<b>Version             :</b> <code>{certain_sheet_version}</code>
<b>Last Modified       :</b> <code>{certain_sheet_modified_time}</code>
<b>Created on          :</b> <code>{certain_sheet_created_time}</code></code>

<b>Stats of</b> <a href="{SMOKE_SHEET_URL}">{SMOKE_INDEX_NAME}</a>

<code><b>Series              :</b> <code>{smoke_total_series}</code>
<b>Movies              :</b> <code>{smoke_total_movies}</code>
<b>Version             :</b> <code>{smoke_sheet_version}</code>
<b>Last Modified       :</b> <code>{smoke_sheet_modified_time}</code>
<b>Created on          :</b> <code>{smoke_sheet_created_time}</code></code>

"""
