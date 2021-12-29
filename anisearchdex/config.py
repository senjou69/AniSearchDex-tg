# ----------BOT------------
OWNER_ID = 0
BOT_TOKEN = ""
USERNAME = ''
SERVICE_ACCOUNT_FILE = ''
# -------------------------


# -------------------------SCOPES----------------------------------
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive.readonly']
SCOPES_SHEET = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# -----------------------------------------------------------------


# --------------------SMOKE INDEX------------------------
SMOKE_INDEX_NAME = "Smoke's Index"
SMOKE_SERIES_RANGE = "B3:I"
SMOKE_MOVIES_RANGE = "Movies!B3:I"
SMOKE_SERIES_STATS_RANGE = "B3:B"
SMOKE_MOVIES_STATS_RANGE = "Movies!B3:B"
SMOKE_SHEET_ID = "1emW2Zsb0gEtEHiub_YHpazvBd4lL4saxCwyPhbtxXYM"
SMOKE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1emW2Zsb0gEtEHiub_YHpazvBd4lL4saxCwyPhbtxXYM"
# --------------------------------------------------------


# --------------------FANSUB INDEX-----------------------
FANSUB_INDEX_NAME = "Fansubber's Index"
FANSUB_SERIES_RANGE = "A2:H"
FANSUB_MOVIES_RANGE = "Movies!A2:H"
FANSUB_SERIES_STATS_RANGE = "A2:A"
FANSUB_MOVIES_STATS_RANGE = "Movies!A2:A"
FANSUB_SHEET_ID = "1PJYwhjzLNPXV2X1np-S4rdZE4fb7pxp-QbHY1O0jH6Q"
FANSUB_SHEET_URL = "https://docs.google.com/spreadsheets/d/1PJYwhjzLNPXV2X1np-S4rdZE4fb7pxp-QbHY1O0jH6Q"
# --------------------------------------------------------


# ----------------- TIMEOUTS (seconds) ---------------------
SESSION_TIMEOUT = 30
CMD_TIMEOUT = 30
# ------------------------------------------------

# ------------------ HELP MSG -------------------
HELP_TEXT = """
<b>Available Commands:</b>
/series  <code> - search for anime series</code>
/movies<code> - search for anime movies</code>
/expose<code> - search release by tags</code>
/stats  <code>  - check stats of indexes</code>
"""
# -----------------------------------------------

# ---- BETTER NOT TOUCH -----
LOG_FILE_NAME = 'anisearchdex_log.txt'
NULL_MSG = "<code>Null</code>"
EMPTY_QUERY_MSG = "<b>Type Something :/</b>"
WELCOME_MSG = "<b>Hey there! Get started by</b> /help"
SEARCH_MSG = '<b>Search</b> <code>{}</code> <b>in</b>'
SESSION_EXP_MSG = "Session Expired."
NO_PAGE_MSG = 'This is the end. 🙂'
TRASH_EMOJI = "🗑"
NO_RESULT_MSG = '<b>No results found :(</b>'
INTRUDER_MSG = "This isn't for you -__-"
# ---------------------------
