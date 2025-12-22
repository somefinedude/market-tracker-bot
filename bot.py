import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from fetcher import MarketFetcher


class MarketBot:
    def __init__(self, token: str, fetcher: MarketFetcher):
        self.fetcher = fetcher

        self.app = (
            ApplicationBuilder()
            .token(token)
            .post_init(self._on_startup)
            .post_shutdown(self._on_shutdown)
            .build()
        )

        self._register_handlers()

    # -------------------- LIFECYCLE --------------------

    async def _on_startup(self, app):
        await self.fetcher.prewarm()
        print("Bot started and cache prewarmed")

    async def _on_shutdown(self, app):
        await self.fetcher.close()
        print("Bot shut down cleanly")

    # -------------------- HANDLERS --------------------

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_custom_pair_input)
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton("ℹ️ Info", callback_data="info"),
                InlineKeyboardButton("📊 Market", callback_data="market"),
            ]
        ]

        await update.message.reply_text(
            text=(
                "*🚀 Welcome to Market Price Tracker Bot!*\n\n"
                "Prices update near real-time.\n"
                "Data from reliable sources."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        handlers = {
            "start": self._start_menu,
            "market": self._market_menu,
            "info": self._info_menu,
            "currencies": self._currencies_menu,
            "metals": self._metals_menu,
            "gold": self._gold,
            "silver": self._silver,
            "usdrub": lambda q: self._currency(q, "RUB"),
            "usdjpy": lambda q: self._currency(q, "JPY"),
            "usdeur": lambda q: self._currency(q, "EUR"),
            "usduzs": lambda q: self._currency(q, "UZS"),
            "usdaud": lambda q: self._currency(q, "AUD"),
            "usdgbp": lambda q: self._currency(q, "GBP"),
            "custompair": self.custompair,
        }

        handler = handlers.get(query.data)
        if handler:
            await handler(query)

    # -------------------- MENUS --------------------

    async def _start_menu(self, query):
        keyboard = [
            [
                InlineKeyboardButton("ℹ️ Info", callback_data="info"),
                InlineKeyboardButton("📊 Market", callback_data="market"),
            ]
        ]

        await query.edit_message_text(
            text=(
                "*🚀 Welcome to Market Price Tracker Bot!*\n\n"
                "Prices update near real-time.\n"
                "Data from reliable sources."
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def _market_menu(self, query):
        keyboard = [
            [InlineKeyboardButton("🪙 Metals", callback_data="metals")],
            [InlineKeyboardButton("💵 Currencies", callback_data="currencies")],
            [InlineKeyboardButton("🔙 Go back", callback_data="start")],
        ]

        await query.edit_message_text(
            "📊 *Market*\n\nChoose a category 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


    async def _silver(self, query):
        data = await self.get_latest_gold()

        text = (
            "📌 *Silver (Live)*\n\n"
            f"💲 {data['silver_usd']} USD / oz\n"
            f"⚖️ Change: {data['silver_change']} USD ({data['silver_pct']}%)\n"
            f"🕒 Updated: {data['timestamp']}"
        )

        await query.edit_message_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Go back", callback_data="metals")]]
            ),
        )

    # ←←←←← ADD YOUR METHOD HERE ↓↓↓↓↓

    async def _handle_custom_pair_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.strip()
        if "/" not in text:
            return
        parts = text.upper().split("/", 1)
        if len(parts) != 2:
            return
        base, target = parts
        base = base.strip()
        target = target.strip()
        if len(base) != 3 or len(target) != 3 or not base.isalpha() or not target.isalpha():
            await update.message.reply_text(
                "❗ Please use format like AUD/UZS (3-letter codes)",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔙 Back to Currencies", callback_data="currencies")]]
                )
            )
            return
        rate = await self.fetcher.get_custom_pair(base, target)
        if rate is not None:
            reply = f"💱 1 {base} = {rate:.6f} {target}"
        else:
            reply = "⛔ Failed to fetch rate (unsupported pair or service down)"
        await update.message.reply_text(
            reply,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Back to Currencies", callback_data="currencies")]]
            )
        )

    # ←←←←← END OF METHOD

async def _info_menu(self, query):
    text = (
        "*ℹ️ Welcome to Market Price Tracker Bot — your reliable, real-time companion for tracking key financial markets!*\n\n"
        "This bot provides up-to-date prices for precious metals and major currency exchange rates, all sourced from trusted professional APIs. "
        "Everything is updated automatically so you always see the latest data without needing to refresh manually.\n\n"
        
        "🪙 *Precious Metals*\n"
        "Live spot prices for Gold and Silver in USD per troy ounce, including:\n"
        "• Current price\n"
        "• Daily change in USD\n"
        "• Percentage change (%)\n"
        "• Exact update timestamp\n\n"
        
        "💵 *Currencies*\n"
        "Real-time USD-based rates for popular pairs:\n"
        "• USD / RUB\n"
        "• USD / JPY\n"
        "• USD / EUR\n"
        "• USD / UZS\n"
        "• USD / AUD\n"
        "• USD / GBP\n\n"
        
        "🌍 *Custom Currency Pairs*\n"
        "Need any other pair? Just send it in the format `XXX/YYY` (e.g., `AUD/GBP`, `UZS/RUB`, `EUR/JPY`). "
        "The bot will instantly fetch and display the current exchange rate. Over 160 currencies supported!\n\n"
        
        "*Data Sources*\n"
        "• Currency rates: exchangerate-api.com (major pairs) and exchangerate.host (custom pairs)\n"
        "• Gold & Silver prices: goldprice.org live data feed\n\n"
        
        "*Why this bot?*\n"
        "• Fast and lightweight — works instantly via inline keyboards\n"
        "• No ads, no spam, no subscriptions\n"
        "• Designed for daily quick checks by traders, travelers, expats, and anyone interested in markets\n\n"
        
        "*Developed as a personal project to deliver accurate, no-nonsense market data right in Telegram.*\n"
        "Suggestions and feedback are always welcome!\n\n"
        "Dev: @JustPythonMan 🚀"
    )

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go back", callback_data="start")]]
        ),
    )

    async def _currencies_menu(self, query):
        keyboard = [
            [InlineKeyboardButton("USD / RUB", callback_data="usdrub")],
            [InlineKeyboardButton("USD / JPY", callback_data="usdjpy")],
            [InlineKeyboardButton("USD / EUR", callback_data="usdeur")],
            [InlineKeyboardButton("USD / UZS", callback_data="usduzs")],
            [InlineKeyboardButton("USD / AUD", callback_data="usdaud")],
            [InlineKeyboardButton("USD / GBP", callback_data="usdgbp")],
            [InlineKeyboardButton("🌍 Custom pair", callback_data="custompair")],
            [InlineKeyboardButton("🔙 Go back", callback_data="market")],
        ]

        await query.edit_message_text(
            "*💵 Currencies*\n\nChoose a pair:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )



    async def _metals_menu(self, query):
        keyboard = [
            [InlineKeyboardButton("🥇 Gold", callback_data="gold")],
            [InlineKeyboardButton("🔗 Silver", callback_data="silver")],
            [InlineKeyboardButton("🔙 Go back", callback_data="market")],
        ]

        await query.edit_message_text(
            "*🪙 Metals*\n\nChoose a metal:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # -------------------- DATA --------------------

    async def _currency(self, query, code: str):
        rates = {
            "RUB": self.fetcher.get_usd_rub,
            "JPY": self.fetcher.get_usd_jpy,
            "EUR": self.fetcher.get_usd_eur,
            "UZS": self.fetcher.get_usd_uzs,
            "AUD": self.fetcher.get_usd_aud,
            "GBP": self.fetcher.get_usd_gbp,
        }

        rate = await rates[code]()
        text = f"1 USD = {rate} {code}" if rate else "Failed to fetch rate"

        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Go back", callback_data="currencies")]]
            ),
        )

    async def custompair(self, query):
        await query.edit_message_text(
            text="🌍 *Custom pair*\n\nHere you can see exchange rate of your preferred pairs:\nPlease enter pairs in this format:\n`AUD/UZS`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Go back", callback_data="currencies")]]
            ),
        )

    async def _handle_custom_pair_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        text = update.message.text.strip().upper()

        if "/" not in text:
            return

        base, target = text.split("/", 1)

        base = base.strip()
        target = target.strip()

        if not base.isalpha() or not target.isalpha():
            await update.message.reply_text("❗ Use format like AUD/UZS")
            return

        if len(base) != 3 or len(target) != 3:
            await update.message.reply_text("❗ Use format like AUD/UZS")
            return

        rate = await self.fetcher.get_custom_pair(base, target)

        if rate:
            reply = f"💱 1 {base} = {rate:.4f}  {target}"
        else:
            reply = "⚠️ Pair not supported or service temporarily unavailable."

        await update.message.reply_text(
            reply,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Go back", callback_data="currencies")]]
            ),
        )

    async def _gold(self, query):
        gold = await self.fetcher.get_latest_gold()

        text = (
            "📌 *Gold (Live)*\n\n"
            f"💲 {gold['gold_usd']} USD / oz\n"
            f"⚖️ Change: {gold['gold_change']} USD ({gold['gold_pct']}%)\n"
            f"🕒 {gold['timestamp']}"
        )

        await query.edit_message_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Go back", callback_data="metals")]]
            ),
        )

    async def _silver(self, query):
        data = await self.fetcher.get_latest_gold()

        text = (
            "📌 *Silver (Live)*\n\n"
            f"💲 {data['silver_usd']} USD / oz\n"
            f"⚖️ Change: {data['silver_change']} USD ({data['silver_pct']}%)\n"
            f"🕒 Updated: {data['timestamp']}"
        )

        await query.edit_message_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 Go back", callback_data="metals")]]
            ),
        )
