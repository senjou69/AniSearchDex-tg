import time
import dateutil.parser

from anisearchdex import message_info
from anisearchdex.config import NULL_MSG, SESSION_TIMEOUT, EMPTY_QUERY_MSG, SMOKE_SERIES_RANGE, SMOKE_MOVIES_RANGE, \
    FANSUB_MOVIES_RANGE, FANSUB_SERIES_RANGE


def cleaner(text):
    return NULL_MSG if (text.isspace() or text.strip() == '') else text.strip()


def isSessionValid(sessionTime):
    elapsed = int(time.time()) - sessionTime
    return True if elapsed < SESSION_TIMEOUT else False


def checkQuery(query):
    if len(query) > 3:
        return True
    elif query != "" and len(query) <= 3:
        return '<b>Query length should be >3 chars :/</b>'
    else:
        return EMPTY_QUERY_MSG


def extractQuery(message):
    try:
        return message.text.split(' ', 1)[1]
    except IndexError:
        return ""


def getSheetRange(whichIndex, whichTab):
    if whichIndex == 'smoke':
        if whichTab == "movies":
            RANGE = SMOKE_MOVIES_RANGE
        elif whichTab == "series":
            RANGE = SMOKE_SERIES_RANGE
    elif whichIndex == 'fansub':
        if whichTab == "movies":
            RANGE = FANSUB_MOVIES_RANGE
        elif whichTab == "series":
            RANGE = FANSUB_SERIES_RANGE
    return RANGE


def cache_clear():
    for i in message_info.copy().items():
        if isSessionValid(i[1][0]) is False:
            message_info.pop(i[0])


def parseIsoDate(well):
    return dateutil.parser.isoparse(well)

