import asyncio
import io
import logging
import os
import re
import sqlite3
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from aiohttp import web  # ✅ FIXED: was "aiiohttp"
from rapidfuzz import process, fuzz
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update,
)
from telegram.constants import ParseMode
from telegram.error import NetworkError, RetryAfter, TimedOut, TelegramError
from telegram.ext import (
    Application, CallbackQueryHandler, CommandHandler, ContextTypes,
    ConversationHandler, MessageHandler, filters,
)
try:
    import psycopg
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("orthodox-bot")

# ✅ FIXED: Use getenv with fallback to prevent crash
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    log.error("BOT_TOKEN environment variable is not set!")
    raise ValueError("BOT_TOKEN environment variable is required")

ADMIN_USER_ID = 7480368503
ADMIN_USERNAME = "@Sealilenemariyammsle12we19"
PRICE = 200
BOT_USERNAME = os.getenv("BOT_USERNAME", "OrthodoxSpiritualBooksBot")
TELEGRAM_CONTACT = "@Sealilenemariyammsle12we19"
EMAIL = "matewosgetahunseifu@gmail.com"
PORT = int(os.getenv("PORT", "10000"))
DATABASE_URL = os.getenv("DATABASE_URL", "")
SQLITE_PATH = os.getenv("SQLITE_PATH", "data/bot.db")

# ✅ FIXED: Ensure data directory exists
Path(SQLITE_PATH).parent.mkdir(parents=True, exist_ok=True)

# Conversation states
SEARCH = 1
RECEIPT = 2
ADMIN_TITLE = 3
ADMIN_CATEGORY = 4

PAYMENT_TEXT = """የኦርቶዶክስ መንፈሳዊ መጽሐፍት ሁሉንም የመጽሐፍ ዓይነቶች (በግዕዝ፣ በአማርኛ፣ 
በግዕዝ አማርኛ፣ የግዕዝ ቋንቋ) ሙሉ በሙሉ ለመጠቀም 200 (ሁለት መቶ) ብር አንድ ጊዜ ብቻ ይክፈሉ። 💳 የክፍያ 
መንገዶች፦ • አሐዱ ባንክ፦ 0100775011101 • የኢትዮጵያ ንግድ ባንክ (CBE)፦ 1000661046841 • አቢሲንያ 
ባንክ፦ 57080698 👤 የአካውንት ስም፦ Matewos Getahun Seifu ክፍያ እንደፈጸሙ የባንክ ሪሲት (Receipt 
Photo/Document) ወደዚህ ቦት ይላኩ።"""

LANGUAGES = {
    "lang_geez": "በግዕዝ",
    "lang_geez_amh": "በግዕዝ አማርኛ",
    "lang_geez_learn": "የግዕዝ ቋንቋ መማሪያ",
    "lang_amh": "በአማርኛ",
    "lang_en": "በእንግሊዝ",
}

CATEGORIES = {
    "lang_geez": {
        "description": "በግዕገ ቋንቋ የህግ እና የስርእት መጽሐፍ ምን ማንበብ ይፈልጋሉ?",
        "cats": {
            "ህግና ስርእት": "በግዕገ ቋንቋ የህግ እና የስርእት መጽሐፍ ምን ማንበብ ይፈልጋሉ?",
            "ታሪክ": "በግዕገ ቋንቋ ከታሪክ መጽሐፍ ምን ማንበብ ይፈልጋሉ?",
            "ገድል ተአምር እና ድርሳን": "በግዕገ ቋንቋ ምን አይነት ገድል ተአምር እና ድርሳን ማንበብ ይፈልጋሉ?",
            "የብሉይ ኪዳን መጻሕፍት": "በግዕገ ቋንቋ ከብሉይ ኪዳን ምን ማንበብ ይፈልጋሉ?",
            "የአዲስ ኪዳን መጻሕፍት": "በግዕገ ቋንቋ ከአዲስ ኪዳን መጻሕፍት ምን ማንበብ ይፈልጋሉ?",
        },
    },
    "lang_geez_amh": {
        "description": "በግዕገ አማርኛ መጽሐፍ ምን ማንበብ ይፈልጋሉ?",
        "cats": {
            "ህግና ስርእት": "በግዕገ አማርኛ የህግና ስርእት መጽሐፍ ምን ማንበብ ይፈልጋሉ?",
            "ታሪክ": "በግዕገ አማርኛ ከታሪክ መጽሐፍ ምን ማንበብ ይፈልጋሉ?",
            "ገድል ተአምር እና ድርሳን": "በግዕገ አማርኛ ምን አይነት ገድል ተአምር እና ድርሳን ማንበብ ይፈልጋሉ?",
            "የብሉይ ኪዳን መጻሕፍት": "በግዕገ አማርኛ ከብሉይ ኪዳን ምን ማንበብ ይፈልጋሉ?",
            "የአዲስ ኪዳን መጻሕፍት": "በግዕገ አማርኛ ከአዲስ ኪዳን ምን ማንበብ ይፈልጋሉ?",
        },
    },
    "lang_geez_learn": {
        "description": "ማንበብ የሚፈልጉ የግእገ ቋንቋ መማሪያ መጽሐፍ ይምረጡ",
        "cats": {"የግዕገ ቋንቋ መማሪያ": "የግዕገ ቋንቋ ማማሪያ"},
    },
    "lang_amh": {
        "description": "በአማርኛ መጽሐፍ ምን ማንበብ ይፈልጋሉ?",
        "cats": {
            "ህግና ስርእት": "የህግና ስርእት መጽሐፍ ይምረጡ",
            "ታሪክ": "ከታሪክ መጽሐፍ ይምረጡ",
            "ድርሳን ተአምር ገድላት": "ድርሳን፣ ተአምር እና ገድላት ይምረጡ",
            "ክርስቲያናዊ ስነምግባር": "የክርስቲያናዊ ስነምግባር መጽሐፍ ይምረጡ",
            "የአዲስ ኪዳን መጽሐፍት": "የአዲስ ኪዳን መፍሐፍት ይምረጡ",
        },
    },
    "lang_en": {
        "description": "Choose a category of English Orthodox spiritual books.",
        "cats": {
            "Law & Order": "Law & Order",
            "History & Discourse": "History & Discourse",
            "Christian Ethics": "Christian Ethics",
            "Bible Study & Passages": "Bible Study & Passages",
            "Theology & Dogma": "Theology & Dogma",
        },
    },
}

SEED_BOOKS = [
    ("ፍትሐ ነገሥት ንባቡና ትርጓሜው", "lang_geez", "ህግና ስርአት", "DUMMY_GA_LAW_01"),
    ("የቤተ ክርስቲያን ሕግና ሥርዓት", "lang_amh", "ህግና ስርአት", "DUMMY_AMH_LAW_01"),
    ("የሥርዓተ ቅዳሴ ማብራሪያ", "lang_amh", "ህግና ስርአት", "DUMMY_AMH_LAW_02"),
    ("የክርስቲያን ሕይወትና ሥርዓት", "lang_amh", "ህግና ስርአት", "DUMMY_AMH_LAW_03"),
    ("ክርስቲያናዊ ሥነ ምግባር", "lang_amh", "ክርስቲያናዊ ስነምግባር", "DUMMY_AMH_ETH_01"),
    ("የሕይወት ጎዳና", "lang_amh", "ክርስቲያናዊ ስነምግባር", "DUMMY_AMH_ETH_02"),
    ("የበጎ አድራጎት ትምህርት", "lang_amh", "ክርስቲያናዊ ስነምግባር", "DUMMY_AMH_ETH_03"),
    ("የትህትናና የፍቅር ሕይወት", "lang_amh", "ክርስቲያናዊ ስነምግባር", "DUMMY_AMH_ETH_04"),
    ("የቤተሰብ ክርስቲያናዊ መመሪያ", "lang_amh", "ክርስቲያናዊ ስነምግባር", "DUMMY_AMH_ETH_05"),
]

for i, category in enumerate(["Law & Order", "History & Discourse", "Christian Ethics", "Bible Study & Passages", "Theology & Dogma"], 1):
    for j in range(1, 6):
        SEED_BOOKS.append((f"{category} Sample {j}", "lang_en", category, f"DUMMY_EN_{i}_{j:02d}"))

def now_iso():
    return datetime.now(timezone.utc).isoformat()

class DB:
    def __init__(self):
        self.pg = bool(DATABASE_URL and POSTGRES_AVAILABLE)
        if not self.pg:
            Path(SQLITE_PATH).parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        else:
            self.conn = None
        self.init()

    def execute(self, sql, params=(), fetch=False, many=False):
        if self.pg:
            sql = sql.replace("?", "%s")
            with psycopg.connect(DATABASE_URL) as c:
                with c.cursor() as cur:
                    if many:
                        cur.executemany(sql, params)
                    else:
                        cur.execute(sql, params)
                    rows = cur.fetchall() if fetch else None
                c.commit()
                return rows
        cur = self.conn.cursor()
        if many:
            cur.executemany(sql, params)
        else:
            cur.execute(sql, params)
            rows = cur.fetchall() if fetch else None
        self.conn.commit()
        return rows

    def init(self):
        id_books = "SERIAL PRIMARY KEY" if self.pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
        id_receipts = "SERIAL PRIMARY KEY" if self.pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
        self.execute("CREATE TABLE IF NOT EXISTS users( user_id BIGINT PRIMARY KEY, username TEXT, is_paid INTEGER DEFAULT 0, registration_date TEXT, referred_by BIGINT, last_seen TEXT)")
        self.execute(f"CREATE TABLE IF NOT EXISTS books( id {id_books}, title TEXT NOT NULL, language TEXT NOT NULL, category TEXT NOT NULL, file_id TEXT, file_key TEXT UNIQUE, created_at TEXT, active INTEGER DEFAULT 1)")
        self.execute(f"CREATE TABLE IF NOT EXISTS receipts( id {id_receipts}, user_id BIGINT, file_id TEXT, file_type TEXT, status TEXT DEFAULT 'pending', created_at TEXT, reviewed_at TEXT)")
        self.execute("CREATE TABLE IF NOT EXISTS progress( user_id BIGINT, book_id INTEGER, page INTEGER DEFAULT 0, updated_at TEXT, PRIMARY KEY(user_id, book_id))")
        self.execute("CREATE TABLE IF NOT EXISTS referrals( referrer_id BIGINT, referred_id BIGINT UNIQUE, created_at TEXT)")
        self.execute("CREATE TABLE IF NOT EXISTS bookmarks( user_id BIGINT, book_id INTEGER, page INTEGER, created_at TEXT, PRIMARY KEY(user_id, book_id, page))")
        for title, lang, cat, key in SEED_BOOKS:
            try:
                self.execute(
                    "INSERT INTO books(title, language, category, file_id, file_key, created_at) VALUES(?,?,?,?,?,?)",
                    (title, lang, cat, None, key, now_iso()),
                )
            except Exception:
                pass

    def upsert_user(self, user_id, username, referred_by=None):
        existing = self.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,), True)
        if existing:
            self.execute("UPDATE users SET username=?, last_seen=? WHERE user_id=?", (username, now_iso(), user_id))
        else:
            self.execute(
                "INSERT INTO users(user_id,username,is_paid,registration_date,referred_by,last_seen) VALUES(?,?,?,?,?,?)",
                (user_id, username, 0, now_iso(), referred_by, now_iso()),
            )
        if referred_by and referred_by != user_id:
            try:
                self.execute("INSERT INTO referrals(referrer_id,referred_id,created_at) VALUES(?,?,?)", (referred_by, user_id, now_iso()))
            except Exception:
                pass

    def is_paid(self, user_id):
        if user_id == ADMIN_USER_ID:
            return True
        rows = self.execute("SELECT is_paid FROM users WHERE user_id=?", (user_id,), True)
        return bool(rows and rows[0][0])

    def set_paid(self, user_id, paid=True):
        self.execute("UPDATE users SET is_paid=? WHERE user_id=?", (1 if paid else 0, user_id))

    def add_receipt(self, user_id, file_id, file_type):
        self.execute("INSERT INTO receipts(user_id, file_id, file_type, created_at) VALUES(?,?,?,?)", (user_id, file_id, file_type, now_iso()))
        rows = self.execute("SELECT id FROM receipts WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,), True)
        return rows[0][0]

    def get_receipt(self, rid):
        rows = self.execute("SELECT id, user_id, file_id, file_type, status FROM receipts WHERE id=?", (rid,), True)
        return rows[0] if rows else None

    def review_receipt(self, rid, status):
        self.execute("UPDATE receipts SET status=?, reviewed_at=? WHERE id=?", (status, now_iso(), rid))

    def books(self, language, category):
        return self.execute("SELECT id,title,file_id,file_key FROM books WHERE language=? AND category=? AND active=1 ORDER BY title", (language, category), True)

    def book(self, book_id):
        rows = self.execute("SELECT id,title,language,category,file_id,file_key FROM books WHERE id=?", (book_id,), True)
        return rows[0] if rows else None

    def all_books(self):
        return self.execute("SELECT id,title,language,category,file_id,file_key FROM books WHERE active=1", (), True)

    def add_book(self, title, language, category, file_id):
        key = f"BOOK_{abs(hash((title, language, category, file_id)) % 10**12)}"
        self.execute("INSERT INTO books(title,language,category,file_id,file_key,created_at) VALUES(?,?,?,?,?,?)", (title, language, category, file_id, key, now_iso()))

    def all_users(self):
        return self.execute("SELECT user_id FROM users", (), True)

    def set_progress(self, user_id, book_id, page):
        if self.pg:
            self.execute("INSERT INTO progress(user_id,book_id,page,updated_at) VALUES(?,?,?,?) ON CONFLICT(user_id,book_id) DO UPDATE SET page=EXCLUDED.page,updated_at=EXCLUDED.updated_at", (user_id, book_id, page, now_iso()))
        else:
            self.execute("INSERT INTO progress(user_id,book_id,page,updated_at) VALUES(?,?,?,?) ON CONFLICT(user_id,book_id) DO UPDATE SET page=excluded.page,updated_at=excluded.updated_at", (user_id, book_id, page, now_iso()))

    def get_progress(self, user_id, book_id):
        rows = self.execute("SELECT page,updated_at FROM progress WHERE user_id=? AND book_id=?", (user_id, book_id), True)
        return rows[0] if rows else None

    def add_bookmark(self, user_id, book_id, page):
        try:
            self.execute("INSERT INTO bookmarks(user_id,book_id,page,created_at) VALUES(?,?,?,?)", (user_id, book_id, page, now_iso()))
            return True
        except Exception:
            return False

    def get_bookmarks(self, user_id, book_id):
        return self.execute("SELECT page,created_at FROM bookmarks WHERE user_id=? AND book_id=? ORDER BY page", (user_id, book_id), True)

db = DB()

def main_keyboard():
    return ReplyKeyboardMarkup([["📚 መጽሐፍት", "🔍 መጽሐፍ ፈልግ"], ["📞 Contact Me", "💬 Feedback"]], resize_keyboard=True)

def language_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("በግዕዝ", callback_data="lang_geez"), InlineKeyboardButton("በግዕዝ አማርኛ", callback_data="lang_geez_amh")],
        [InlineKeyboardButton("የግዕዝ ቋንቋ መማሪያ", callback_data="lang_geez_learn")],
        [InlineKeyboardButton("በአማርኛ", callback_data="lang_amh"), InlineKeyboardButton("በእንግሊዝ", callback_data="lang_en")],
    ])

async def retry_send(action, attempts=5):
    delay = 1
    for _ in range(attempts):
        try:
            return await action()
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except (NetworkError, TimedOut):
            await asyncio.sleep(delay)
            delay = min(delay * 2, 16)
    raise RuntimeError("Telegram delivery failed after retries")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ref = None
    if context.args:
        m = re.fullmatch(r"REF_(\d+)", context.args[0])
        if m:
            ref = int(m.group(1))
    db.upsert_user(user.id, user.username or "", ref)
    await update.message.reply_text("እንኳን ወደ ታላቁ ዲጂታል መጽሃፍት ቦት በሰላም መጡ!", reply_markup=main_keyboard())

async def books_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("እባኮን በምን ቋንቋ መጽሐፍ ማንበብ ይፈልጋሉ?", reply_markup=language_keyboard())

async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = q.data
    context.user_data["language"] = lang
    cfg = CATEGORIES[lang]
    buttons = [[InlineKeyboardButton(name, callback_data=f"cat|{lang}|{name}") for name in list(cfg["cats"].keys())][i:i+2] for i in range(0, len(cfg["cats"]), 2)]
    await q.edit_message_text(cfg["description"], reply_markup=InlineKeyboardMarkup(buttons))

async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, lang, category = q.data.split("|", 2)
    rows = db.books(lang, category)
    if not rows:
        await q.edit_message_text("በዚህ ምድብ ምንም መጽሐፍ የለም። እባኮን ሌላ ምድብ ይምረጡ።")
        return
    buttons = [[InlineKeyboardButton(r[1], callback_data=f"book|{r[0]}") for r in rows]]
    await q.edit_message_text("እባኮን መጽሐፉን ይምረጡ።", reply_markup=InlineKeyboardMarkup(buttons))

async def book_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, book_id = q.data.split("|", 1)
    book = db.book(int(book_id))
    if not book:
        await q.edit_message_text("መጽሐፍ አልተገኘም።")
        return
    context.user_data["selected_book"] = int(book_id)
    buttons = [[InlineKeyboardButton("👁️ Preview", callback_data=f"preview|{book_id}")]]
    if db.is_paid(q.from_user.id):
        buttons.append([InlineKeyboardButton("📖 ሙሉ መጽሐፍ አንብብ", callback_data=f"read|{book_id}")])
    else:
        buttons.append([InlineKeyboardButton("💳 ክፍያ ለማድረግ", callback_data="send_receipt")])
    await q.edit_message_text(f"<b>{book[1]}</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(buttons))

async def send_full_book(chat_id, book, bot):
    if not book[4]:
        await bot.send_message(chat_id, "ይህ መጽሐፍ በስርአቱ ውስጥ አላለፈም። እባኮን አስተዳዳሪውን ያግኙ።")
        return
    await retry_send(lambda: bot.send_document(chat_id, document=book[4], protect_content=True, caption=f"📖 {book[1]}"))

async def read_or_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, book_id = q.data.split("|", 1)
    book = db.book(int(book_id))
    if not book:
        await q.edit_message_text("መጽሐፍ አልተገኘም።")
        return
    if not db.is_paid(q.from_user.id):
        await q.message.reply_text(PAYMENT_TEXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 ሪሲት ላክ", callback_data="send_receipt")], [InlineKeyboardButton("📞 Contact Me", callback_data="contact")]]))
        return
    await send_full_book(q.message.chat_id, book, context.bot)

async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, book_id = q.data.split("|", 1)
    book = db.book(int(book_id))
    if not book:
        return
    if not book[4]:
        await q.message.reply_text("Preview: ይህ የዲሞ መጽሐፍ መዝገብ ነው። PDF ከተጫነ በኋላ የመጀመሪያዎቹ 3 ገጾች ይላካሉ።")
        return
    if fitz is None:
        await q.message.reply_text("Preview ለማመንጨት PyMuPDF አልተጫነም።")
        return
    tg_file = await context.bot.get_file(book[4])
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "book.pdf"
        out = Path(td) / "preview.pdf"
        await tg_file.download_to_drive(custom_path=str(src))
        doc = fitz.open(src)
        preview_doc = fitz.open()
        for i in range(min(3, len(doc))):
            preview_doc.insert_pdf(doc, from_page=i, to_page=i)
        preview_doc.save(out)
        preview_doc.close()
        doc.close()
        with open(out, "rb") as f:
            await q.message.reply_document(f, caption=f"📖 Preview: {book[1]}", protect_content=True)

async def search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 የመጽሐፉን ስም ወይም ቁልፍ ቃል ይጻፉ።")
    return SEARCH

async def do_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    rows = db.all_books()
    titles = [r[1] for r in rows]
    exact = [r for r in rows if query.casefold() == r[1].casefold()]
    matches = exact or [r for r, score, _ in process.extract(query, rows, scorer=lambda q, r: fuzz.WRatio(q, r[1]), limit=8) if score >= 45]
    if not matches:
        await update.message.reply_text("ምንም ተመሳሳይ መጽሐፍ አልተገኘም።")
        return ConversationHandler.END
    buttons = [[InlineKeyboardButton(r[1], callback_data=f"book|{r[0]}")] for r in matches]
    await update.message.reply_text("የተገኙ መጽሐፍት፦", reply_markup=InlineKeyboardMarkup(buttons))
    return ConversationHandler.END

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"📞 Contact Me\nTelegram: {TELEGRAM_CONTACT}\nEmail: {EMAIL}"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text)
    else:
        await update.message.reply_text(text)

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💬 አስተያየትዎን ያድርሱን፦\nለማንኛውም ጥያቄ፣ አስተያየት ወይም ተጨማሪ መጽሐፍ ጥቆማ ያግኙን፦\n"
        f"Telegram: {TELEGRAM_CONTACT}\nEmail: {EMAIL}"
    )

async def receipt_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if q:
        await q.answer()
        await q.message.reply_text("🧾 እባክዎ የባንክ ሪሲቱን ፎቶ ወይም PDF ሰነድ ይላኩ።")
    else:
        await update.message.reply_text("🧾 የባንክ ሪሲቱን ፎቶ ወይም PDF ሰነድ ይላኩ።")
    return RECEIPT

async def receipt_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg.photo:
        file_id = msg.photo[-1].file_id
        typ = "photo"
    elif msg.document:
        file_id = msg.document.file_id
        typ = "document"
    else:
        await msg.reply_text("እባክዎ ፎቶ ወይም PDF/document ይላኩ።")
        return RECEIPT
    rid = db.add_receipt(msg.from_user.id, file_id, typ)
    admin_text = f"🧾 New payment receipt\nReceipt ID: {rid}\nUser ID: {msg.from_user.id}\nUsername: @{msg.from_user.username or 'none'}"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ APPROVE", callback_data=f"approve|{rid}"), InlineKeyboardButton("❌ REJECT", callback_data=f"reject|{rid}")]
    ])
    if typ == "photo":
        await context.bot.send_photo(ADMIN_USER_ID, file_id, caption=admin_text, reply_markup=kb)
    else:
        await context.bot.send_document(ADMIN_USER_ID, file_id, caption=admin_text, reply_markup=kb)
    await msg.reply_text("ሪሲቱ ተቀብሏል። አስተዳዳሪው ካረጋገጠ በኋላ መጽሐፍቱን ሙሉ በሙሉ ማንበብ ይችላሉ።")
    return ConversationHandler.END

async def review_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.from_user.id != ADMIN_USER_ID:
        return
    action, rid_s = q.data.split("|", 1)
    rid = int(rid_s)
    row = db.get_receipt(rid)
    if not row:
        await q.edit_message_caption(caption="Receipt not found.")
        return
    approved = action == "approve"
    db.review_receipt(rid, "approved" if approved else "rejected")
    if approved:
        db.set_paid(row[1], True)
        await context.bot.send_message(row[1], "✅ ክፍያዎ ተረጋግጧል። አሁን ሁሉንም መጽሐፍት መጠቀም ይችላሉ።")
    else:
        await context.bot.send_message(row[1], "❌ ሪሲቱ አልተረጋገጠም። እባክዎ ትክክለኛ ሪሲት እንደገና ይላኩ።")
    await q.edit_message_caption(caption=f"Receipt #{rid}: {'APPROVED' if approved else 'REJECTED'}")

async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text(
        "🛠 Admin Panel\n"
        "/uploadbook — upload a PDF and register it\n"
        "/broadcast — broadcast a text message\n"
        "/stats — user/book/payment statistics"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return
    users = len(db.all_users())
    books = len(db.all_books())
    await update.message.reply_text(f"Users: {users}\nBooks: {books}")

async def upload_book_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        return ConversationHandler.END
    await update.message.reply_text("Send the PDF file now.")
    return ADMIN_TITLE

async def upload_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID or not update.message.document:
        await update.message.reply_text("Please send a PDF document.")
        return ADMIN_TITLE
    doc = update.message.document
    if doc.mime_type != "application/pdf" and not (doc.file_name or "").lower().endswith("pdf"):
        await update.message.reply_text("Only PDF files are accepted.")
        return ADMIN_TITLE
    context.user_data["upload_file_id"] = doc.file_id
    context.user_data["upload_name"] = doc.file_name or "book.pdf"
    await update.message.reply_text("Now send the book title.")
    return ADMIN_CATEGORY

async def upload_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["upload_title"] = update.message.text.strip()
    await update.message.reply_text("Send category path as:\nLANGUAGE | CATEGORY\n\nExample: lang_en | Theology & Dogma")
    return ADMIN_CATEGORY + 1

async def upload_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = update.message.text.strip()
    if "|" not in raw:
        await update.message.reply_text("Format must be LANGUAGE | CATEGORY")
        return ADMIN_CATEGORY + 1
    lang, category = [x.strip() for x in raw.split("|", 1)]
    if lang not in CATEGORIES or category not in CATEGORIES[lang]["cats"]:
        await update.message.reply_text("Invalid language/category path. Try again.")
        return ADMIN_CATEGORY + 1
    db.add_book(context.user_data["upload_title"], lang, category, context.user_data["upload_file_id"])
    await update.message.reply_text("✅ Book registered and added dynamically to the category UI.")
    for row in db.all_users():
        uid = row[0]
        try:
            await retry_send(lambda uid=uid: context.bot.send_message(uid, "🆕 አዲስ መጽሐፍ ተጨምሯል!"))
        except Exception:
            log.warning("Broadcast failed for user %s", uid)
    return ConversationHandler.END

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    me = await context.bot.get_me()
    link = f"https://t.me/{me.username}?start=REF_{update.effective_user.id}"
    await update.message.reply_text(f"🔗 የማጋራት ሊንክዎ፦\n{link}")

async def generic_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📚 መጽሐፍት":
        await books_menu(update, context)
    elif text == "🔍 መጽሐፍ ፈልግ":
        await search_start(update, context)
    elif text == "📞 Contact Me":
        await contact(update, context)
    elif text == "💬 Feedback":
        await feedback(update, context)

async def save_progress_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /progress BOOK_ID PAGE")
        return
    try:
        book_id, page = int(context.args[0]), int(context.args[1])
    except ValueError:
        await update.message.reply_text("BOOK_ID and PAGE must be numbers.")
        return
    if not db.book(book_id):
        await update.message.reply_text("Book not found.")
        return
    db.set_progress(update.effective_user.id, book_id, max(0, page))
    await update.message.reply_text(f"Reading progress saved: page {max(0, page)}")

async def add_bookmark_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /bookmark BOOK_ID PAGE")
        return
    try:
        book_id, page = int(context.args[0]), int(context.args[1])
    except ValueError:
        await update.message.reply_text("BOOK_ID and PAGE must be numbers.")
        return
    if not db.book(book_id):
        await update.message.reply_text("Book not found.")
        return
    if db.add_bookmark(update.effective_user.id, book_id, max(0, page)):
        await update.message.reply_text("Bookmark saved.")
    else:
        await update.message.reply_text("That bookmark already exists.")

async def show_progress_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /progresses BOOK_ID")
        return
    try:
        book_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("BOOK_ID must be a number.")
        return
    book = db.book(book_id)
    if not book:
        await update.message.reply_text("Book not found.")
        return
    prog = db.get_progress(update.effective_user.id, book_id)
    marks = db.get_bookmarks(update.effective_user.id, book_id)
    page = prog[0] if prog else 0
    mark_text = ", ".join(str(r[0]) for r in marks) if marks else "none"
    await update.message.reply_text(
        f"📖 {book[1]}\nProgress: page {page}\nBookmarks: {mark_text}"
    )

async def health(request):
    return web.json_response({"status": "ok", "service": "OrthodoxSpiritualBooksBot"})

async def run_health_server():
    app = web.Application()
    app.router.add_get("/health", health)
    app.router.add_get("/ping", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    log.info("Health server listening on %s", PORT)
    # ✅ FIXED: Keep the server running without infinite loop
    await asyncio.Event().wait()  # Wait forever

async def post_init(application):
    asyncio.create_task(run_health_server())

def build_app():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    search_conv = ConversationHandler(
        entry_points=[CommandHandler("search", search_start), MessageHandler(filters.Regex("^🔍 መጽሐፍ ፈልግ$"), search_start)],
        states={SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, do_search)]},
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    receipt_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(receipt_start, pattern="^send_receipt$")],
        states={RECEIPT: [MessageHandler(filters.PHOTO | filters.Document.ALL, receipt_received)]},
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    upload_conv = ConversationHandler(
        entry_points=[CommandHandler("uploadbook", upload_book_start)],
        states={
            ADMIN_TITLE: [MessageHandler(filters.Document.PDF | filters.Document.ALL, upload_pdf)],
            ADMIN_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_title)],
            ADMIN_CATEGORY + 1: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_category)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_cmd))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CommandHandler("progress", save_progress_cmd))
    app.add_handler(CommandHandler("bookmark", add_bookmark_cmd))
    app.add_handler(CommandHandler("progresses", show_progress_cmd))
    app.add_handler(search_conv)
    app.add_handler(receipt_conv)
    app.add_handler(upload_conv)
    app.add_handler(CallbackQueryHandler(language_selected, pattern=r"^lang_"))
    app.add_handler(CallbackQueryHandler(category_selected, pattern=r"^cat\|"))
    app.add_handler(CallbackQueryHandler(book_selected, pattern=r"^book\|"))
    app.add_handler(CallbackQueryHandler(preview, pattern=r"^preview\|"))
    app.add_handler(CallbackQueryHandler(read_or_payment, pattern=r"^read\|"))
    app.add_handler(CallbackQueryHandler(review_receipt, pattern=r"^(approve|reject)\|"))
    app.add_handler(CallbackQueryHandler(contact, pattern=r"^contact$"))
    app.add_handler(MessageHandler(filters.Regex("^📚 መጽሐፍት$"), books_menu))
    app.add_handler(MessageHandler(filters.Regex("^📞 Contact Me$"), contact))
    app.add_handler(MessageHandler(filters.Regex("^💬 Feedback$"), feedback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generic_text))
    return app

if __name__ == "__main__":
    application = build_app()
    application.run_polling(allowed_updates=Update.ALL_TYPES)