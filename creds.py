from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")
BASE_URL = os.getenv("BASE_URL")
DEV_CHAT_ID = os.getenv("DEV_CHAT_ID")
GPT_TOKEN = os.getenv("GPT_TOKEN")
