import os
from fetcher import MarketFetcher
from bot import MarketBot
from dotenv import load_dotenv
load_dotenv()
fetcher = MarketFetcher(
    exchange_api_key=os.getenv("EXCHANGE_API_KEY")
)

bot = MarketBot(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    fetcher=fetcher,
)

print("TELEGRAM:", os.getenv("TELEGRAM_BOT_TOKEN"))
print("EXCHANGE:", os.getenv("EXCHANGE_API_KEY"))
bot.run()
