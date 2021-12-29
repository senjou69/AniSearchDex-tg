import asyncio
import logging
import os
import time

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from google.oauth2 import service_account
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from anisearchdex.config import SERVICE_ACCOUNT_FILE, SCOPES_DRIVE, SCOPES_SHEET, BOT_TOKEN, LOG_FILE_NAME

botStartTime = time.time()
message_info = dict()
storage = MemoryStorage()
callback_lock = asyncio.Lock()

if os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(LOG_FILE_NAME), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# --------SHEET SERVICE BUILDER------------
try:
    sheet_creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES_SHEET)
    sheet_service = build('sheets', 'v4', credentials=sheet_creds).spreadsheets()
    LOGGER.info("Successfully built Sheet service")
except:
    LOGGER.error("Failed to build Sheet service")
# -----------------------------------


# ---------DRIVE SERVICE BUILDER-------------
try:
    drive_creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES_DRIVE)
    drive_service = build('drive', 'v3', credentials=drive_creds)
    LOGGER.info("Successfully built Drive service")
except:
    LOGGER.error("Failed to build Drive service")
# -----------------------------------


bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
