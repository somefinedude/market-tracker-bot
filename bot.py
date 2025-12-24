import os
from db import log_user
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

        # Initialize the Application
        self.app = (
            ApplicationBuilder()
            .token(token)
            .build()
        )

        self._register_handlers()

    # ############################# HANDLERS #####################################################################################################################

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
        # This handler catches the custom pair text input (e.g., AUD/UZS)
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_custom_pair_input)
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        log_user(update.effective_user)
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

    # ############################# MENUS ####################################################################################################################

    async def _start_menu(self, query):
        keyboard = [
            [
                InlineKeyboardButton("ℹ️ Info", callback_data="info"),
                InlineKeyboardButton("📊 Market", callback_data="market"),
            ]
        ]
        await query.edit_message_text(
            text="*🚀 Welcome to Market Price Tracker Bot!*",
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
        text = (
            "*ℹ️ Welcome to Market Price Tracker Bot!*\n\n"
            "This bot provides up-to-date prices for precious metals and currencies.\n\n"
            "🪙 *Precious Metals*\n"
            "Live spot prices for Gold and Silver in USD.\n\n"
            "💵 *Currencies*\n"
            "Real-time USD-based rates for popular pairs.\n\n"
            "🌍 *Custom Currency Pairs*\n"
            "Format: `XXX/YYY` (e.g., `AUD/GBP`).\n\n"
            "Dev: @JustPythonMan 🚀"
        )
        await query.edit_message_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go back", callback_data="start")]]),
        )

    async def _currencies_menu(self, query):
        keyboard = [
            [InlineKeyboardButton("USD / RUB", callback_data="usdrub")],
            [InlineKeyboardButton("USD / EUR", callback_data="usdeur")],
            [InlineKeyboardButton("USD / UZS", callback_data="usduzs")],
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

    # ############################### DATA LOGIC #######################################################################################################################

    async def _currency(self, query, code: str):
        # Maps codes to fetcher methods
        rates_map = {
            "RUB": self.fetcher.get_usd_rub,
            "JPY": self.fetcher.get_usd_jpy,
            "EUR": self.fetcher.get_usd_eur,
            "UZS": self.fetcher.get_usd_uzs,
            "AUD": self.fetcher.get_usd_aud,
            "GBP": self.fetcher.get_usd_gbp,
        }
        rate = await rates_map[code]()
        text = f"1 USD = {rate} {code}" if rate else "Failed to fetch rate"
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go back", callback_data="currencies")]]),
        )

    async def custompair(self, query):
        await query.edit_message_text(
            text="🌍 *Custom pair*\n\nPlease enter pairs in this format:\n`AUD/UZS`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go back", callback_data="currencies")]]),
        )

    async def _handle_custom_pair_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.strip().upper()
        if "/" not in text: return

        try:
            base, target = text.split("/", 1)
            base, target = base.strip(), target.strip()

            if len(base) == 3 and len(target) == 3 and base.isalpha() and target.isalpha():
                rate = await self.fetcher.get_custom_pair(base, target)
                reply = f"💱 1 {base} = {rate:.4f} {target}" if rate else "⚠️ Pair not supported."
            else:
                reply = "❗ Use format like AUD/UZS (3-letter codes)"
        except Exception:
            reply = "❗ Error processing request. Use format XXX/YYY."

        await update.message.reply_text(
            reply,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go back", callback_data="currencies")]])
        )

    async def _gold(self, query):
        gold = await self.fetcher.get_latest_gold()
        text = (
            "📌 *Gold (Live)*\n\n"
            f"💲 {gold['gold_usd']} USD / oz\n"
            f"⚖️ Change: {gold['gold_change']} USD ({gold['gold_pct']}%)\n"
            f"🕒 {gold['timestamp']}"
        )
        await query.edit_message_text(text=text, parse_mode="Markdown",
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go back", callback_data="metals")]]))

    async def _silver(self, query):
        data = await self.fetcher.get_latest_gold()
        text = (
            "📌 *Silver (Live)*\n\n"
            f"💲 {data['silver_usd']} USD / oz\n"
            f"⚖️ Change: {data['silver_change']} USD ({data['silver_pct']}%)\n"
            f"🕒 Updated: {data['timestamp']}"
        )
        await query.edit_message_text(text=text, parse_mode="Markdown",
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Go back", callback_data="metals")]]))