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
            "custompair": self.custom_pair_prompt,
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

    async def _info_menu(self, query):
        await query.edit_message_text(
            "*ℹ️ Info*\n\nThis bot tracks market prices.",
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
            [InlineKeyboardButton("🌍 Custom pair", callback_data="custom_pair_info")],
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

    async def custom_pair_prompt(self, query):
        await query.edit_message_text(
            text="🌍 *Custom pair*\n\nSend pair like:\n`AUD/UZS`",
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

        if len(base) != 3 or len(target) != 3:
            await update.message.reply_text("❗ Use format like AUD/UZS")
            return

        rate = await self.fetcher.get_custom_pair(base, target)

        if rate:
            reply = f"💱 1 {base} = {rate} {target}"
        else:
            reply = "⛔ Failed to fetch exchange rate"

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
