import os

from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
db_dsn = os.getenv("DB_DSN")
pool_size = os.getenv("DB__POOL_SIZE")
max_overflow = os.getenv("DB__MAX_OVERFLOW")
pool_pre_ping = os.getenv("DB__POOL_PRE_PING")
connection_timeout = os.getenv("DB__CONNECTION_TIMEOUT")
command_timeout = os.getenv("DB__COMMAND_TIMEOUT")
app_name = os.getenv("DB__APP_NAME")
timezone = os.getenv("DB__TIMEZONE")
