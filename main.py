import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from bot import Bot, web_app, run_flask
from pyrogram import compose
from config import *
from threading import Thread

# 🚀 Start Flask FIRST for Render health check
Thread(target=run_flask, daemon=True).start()

async def main():
    app = []

    app.append(
        Bot(
            SESSION,
            WORKERS,
            DB_CHANNEL,
            FSUBS,
            TOKEN,
            ADMINS,
            MESSAGES,
            AUTO_DEL,
            DB_URI,
            DB_NAME,
            API_ID,
            API_HASH,
            PROTECT,
            DISABLE_BTN
        )
    )

    await compose(app)

async def runner():
    await asyncio.gather(
        main(),
        web_app()
    )

asyncio.run(runner())
