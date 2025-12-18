import os
from fetcher import MarketFetcher
from bot import MarketBot

fetcher = MarketFetcher(
    exchange_api_key=os.getenv("EXCHANGE_API_KEY")
)

bot = MarketBot(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    fetcher=fetcher,
)

bot.run()
