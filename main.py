from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from telegram import Update
from bot import MarketBot
from fetcher import MarketFetcher
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Init Fetcher
    fetcher = MarketFetcher(exchange_api_key=os.getenv("EXCHANGE_API_KEY"))
    await fetcher.prewarm()

    # 2. Init Bot
    bot_app = MarketBot(token=os.getenv("TELEGRAM_BOT_TOKEN"), fetcher=fetcher)
    await bot_app.app.initialize()
    await bot_app.app.start()
    await bot_app.app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    app.state.bot_app = bot_app
    app.state.fetcher = fetcher
    
    yield

    # 3. Shutdown
    await bot_app.app.stop()
    await bot_app.app.shutdown()
    await fetcher.close()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, app.state.bot_app.app.bot)
    await app.state.bot_app.app.process_update(update)
    return {"ok": True}