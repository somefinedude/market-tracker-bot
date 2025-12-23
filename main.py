from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from telegram import Update
from bot import MarketBot
from fetcher import MarketFetcher
import os
import asyncio
import httpx


WEBHOOK_URL = os.getenv("WEBHOOK_URL")


async def keep_alive_loop():
    await asyncio.sleep(30)
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(f"{WEBHOOK_URL.rstrip('/')}/health")
                print(f"Self-ping status: {response.status_code}")
            except Exception as e:
                print(f"Self-ping failed: {e}")
            await asyncio.sleep(600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    fetcher = MarketFetcher(exchange_api_key=os.getenv("EXCHANGE_API_KEY"))
    await fetcher.prewarm()

    bot_app = MarketBot(token=os.getenv("TELEGRAM_BOT_TOKEN"), fetcher=fetcher)
    await bot_app.app.initialize()
    await bot_app.app.start()
    await bot_app.app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    asyncio.create_task(keep_alive_loop())
    app.state.bot_app = bot_app
    app.state.fetcher = fetcher
    
    yield

    await bot_app.app.stop()
    await bot_app.app.shutdown()
    await fetcher.close()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "alive", "msg": "I am awake"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, app.state.bot_app.app.bot)
    await app.state.bot_app.app.process_update(update)
    return {"ok": True}