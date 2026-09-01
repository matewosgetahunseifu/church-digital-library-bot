import os
import sqlite3
import pytesseract
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ==========================================
# 1. CONFIGURATION & ENVIRONMENT SETUP
# ==========================================

# Telegram Chat ID እና Bot Token (በደህንነት ምክንያት ከ Environment Variable ቢያነብ ይመረጣል)
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", 7480368503))
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8777005011:AAHi7FXjLXk9QkRBzylmzsLqYj7dRC1PR_Y")

# Render (Linux Server) ላይ Tesseract Pathን በራስ-ሰር ለመለየት
if os.path.exists('/usr/bin/tesseract'):
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# ==========================================
# 2. SQLITE DATABASE SETUP
# ==========================================

def init_db():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approved_users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT
        )
    """)
    conn.commit()
    conn.close()

def is_user_approved(user_id: int) -> bool:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM approved_users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_approved_user(user_id: int, username: str, full_name: str):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO approved_users VALUES (?, ?, ?)", (user_id, username, full_name))
    conn.commit()
    conn.close()

def remove_approved_user(user_id: int):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM approved_users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_approved_users():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM approved_users")
    users = cursor.fetchall()
    conn.close()
    return [u[0] for u in users]

# ==========================================
# 3. COMPLETE BOOKS & MENU STRUCTURE
# ==========================================

MENU_STRUCTURE = {
    "📜 ግእዝ": {
        "ሕግና ሥርዓት": {"books": []},
        "ታሪክና ድርሳናት": {
            "ታሪክ": {"books": []},
            "ድርሳን፣ ገድልና ተአምር": {"books": []}
        },
        "ክርስቲያናዊ ሥነ ምግባር": {"books": []},
        "የመጽሐፍ ቅዱስ ክፍል": {
            "የብሉይ ኪዳን መጻሕፍት": {
                "books": [
                    {
                        "id": "gz_ot_1",
                        "title": "፭ቱ መጽሐፈ ኦሪት ብራና አንድምታ",
                        "file_id": "BQACAgQAAxkBAAP4apL8OXANqEqvyGn7V4Lk_C1rDygAAn0JAAIWA9hQayRhNPpVNvE9BA"
                    }
                ]
            },
            "የሐዲስ ኪዳን መጻሕፍት": {"books": []}
        }
    },
    "🇪🇹 ግእዝ-አማርኛ": {
        "ሕግና ሥርዓት": {"books": []},
        "ታሪክና ድርሳናት": {
            "ታሪክ": {"books": []},
            "ድርሳን፣ ገድልና ተአምር": {"books": []}
        },
        "ክርስቲያናዊ ሥነ ምግባር": {"books": []},
        "የመጽሐፍ ቅዱስ ክፍል": {
            "የብሉይ ኪዳን መጻሕፍት": {
                "books": [
                    {
                        "id": "ga_ot_1",
                        "title": "ኦሪት ዘፍጥረት አንድምታ",
                        "file_id": "BQACAgQAAxkBAAPoapL5-j4Y4yKee0lyFZlMHif5UoAAAgcKAAKjPElSpWxXt7rSOxk9BA"
                    },
                    {
                        "id": "ga_ot_2",
                        "title": "ኦሪት ዘፀአት አንድምታ",
                        "file_id": "BQACAgQAAxkBAAPpapL5-mx2OLB_jMKwjJx8isE-LRAAAggKAAKjPElSdkt4uS3PouI9BA"
                    },
                    {
                        "id": "ga_ot_3",
                        "title": "ኦሪት ዘሌዋውያን አንድምታ",
                        "file_id": "BQACAgQAAxkBAAPqapL5-mUjkfP8bzTvar9D5ZmjeIwAAvUKAAL6HClR9oG7Bfn__tI9BA"
                    },
                    {
                        "id": "ga_ot_4",
                        "title": "ኦሪት ዘኍልቅ አንድምታ",
                        "file_id": "BQACAgQAAxkBAAPrapL5-vSTNfOEAAEE0CwlPjz-oH1cAAIKCgACozxJUstPvw26Lpm9PQQ"
                    },
                    {
                        "id": "ga_ot_5",
                        "title": "ኦሪት ዘዳግም አንድምታ",
                        "file_id": "BQACAgQAAxkBAAPsapL5-qt3Lcu5lWpCIB8LZ9ly_V8AAgsKAAKjPElSKmH6OAPSIR49BA"
                    }
                ]
            },
            "የሐዲስ ኪዳን መጻሕፍት": {"books": []}
        }
    },
    "📖 የግእዝ ቋንቋ መማሪያ": {
        "books": [
            {
                "id": "l_1",
                "title": "መጽሐፈ ሰዋስው ወግስ ወመዝገበ ቃላት ሐዲስ (አለቃ ኪዳነ ወልድ ክፍሌ)",
                "file_id": "BQACAgQAAxkBAAOiapLEYe5R4ZxJ8_3PQZ-SHO6NA4sAAqofAAI12zhQV3FkwrOJJtc9BA"
            },
            {
                "id": "l_2",
                "title": "ግእዝ እንግሊዝኛ ኦገስት ዲልማን",
                "file_id": "BQACAgQAAxkBAAOvapLOTuM_iJ5-xleFbnGNgDLeJzAAAqAhAAKba2BQb49RMRsZf_49BA"
            },
            {
                "id": "l_3",
                "title": "ግስ እምባቆብ",
                "file_id": "BQACAgQAAxkBAAOxapLOToEwCL4K_RHREKweqU9_buMAAlgGAALy24lQiHGMdWTQj_I9BA"
            },
            {
                "id": "l_4",
                "title": "መጽሐፈ ግእዝ",
                "file_id": "BQACAgQAAxkBAAOyapLOTqigZoRB37TkUs3YBzjgx0oAAmwQAAKDKPFTW2HbAekftKU9BA"
            },
            {
                "id": "l_5",
                "title": "ጥንታዊ ግእዝ በዘመናዊ አቀራረብ (ካልኣይ ክፍል)",
                "file_id": "BQACAgQAAxkBAAOwapLOTnyZqs5q3YoQooXwdQLLdhkAAqUhAAKba2BQrTKlP3O6ohg9BA"
            },
            {
                "id": "l_6",
                "title": "ትንሳዔ ግእዝ (መምህር ደሴ ቀለብ)",
                "file_id": "BQACAgQAAxkBAAOzapLOTgKDH7A6tfXemG-zjjdcj8oAAvsBAAKh56lQKVEyEdzzV7Y9BA"
            },
            {
                "id": "l_7",
                "title": "ፍሬ ግእዝ",
                "file_id": "BQACAgQAAxkBAAO0apLOTkraJZeY7MMSjeoRi9huctAAAvEQAAL0ZllRd1T8Cz3MfR89BA"
            },
            {
                "id": "l_8",
                "title": "ግእዝ እንበለ መምህር",
                "file_id": "BQACAgQAAxkBAAO1apLOTgLec1zclkRUTQU9IcZIAeMAAlsZAALmW4FQynTLeSEqAZQ9BA"
            },
            {
                "id": "l_9",
                "title": "የግእዝ ሰዋሰው (ዓለማየሁ ሞገስ)",
                "file_id": "BQACAgQAAxkBAAO2apLOTl-cs3ftddnQSFcTg0ZxE1cAAoshAAKba2BQCmlU5vYhiKo9BA"
            },
            {
                "id": "l_10",
                "title": "ግእዝ መማሪያ መጽሐፍ",
                "file_id": "BQACAgQAAxkBAAO3apLOTm6QfeRlG6uKjTMJ4zx96ooAAocHAAJyFMhT0rbd1ZaTvsY9BA"
            },
            {
                "id": "l_11",
                "title": "ግዕዝ መሠረተ ትምህርት (ደስታ ተክለወልድ)",
                "file_id": "BQACAgQAAxkBAAO4apLOTpmweUFZNie-aTlg5hoTx2MAAqECAAKpJdlS5zKDZrrocvA9BA"
            },
            {
                "id": "l_12",
                "title": "የግእዝ መማሪያ (ዶ/ር ለይኩን ብርሀኑ)",
                "file_id": "BQACAgQAAxkBAAO5apLOTn5wYdAKlzCSp2FmCNQD_-YAArUGAAJv75lRsafLj8CJxmM9BA"
            },
            {
                "id": "l_13",
                "title": "ሰዋስወ ግእዝ ወአንቀጽ",
                "file_id": "BQACAgQAAxkBAAO6apLOToQiuej6WJBDqZP3j_YAAWppAALKFQAC2aVxUmuX4vLb4xyBPQQ"
            },
            {
                "id": "l_14",
                "title": "መርኆ ሰዋስው ዘልሳነ ግእዝ",
                "file_id": "BQACAgQAAxkBAAO7apLOTluw2HKlQ3pbSGzD2_riMcIAAikYAAJds_lQWZXHtP7ylCE9BA"
            },
            {
                "id": "l_15",
                "title": "መዝገበ ግስ (ሁሉንም ግስ በአንድ የያዘ)",
                "file_id": "BQACAgQAAxkBAAO8apLOTjpUoaE4ZWHGHe813QABMrsyAALWGAACm_fpUfxpVw9o_4grPQQ"
            },
            {
                "id": "l_16",
                "title": "መጽሐፈ ሰዋስው",
                "file_id": "BQACAgQAAxkBAAO9apLOThplHgQeqctpal2rVuqMU-8AAq8cAAIe9uFQcwlbPLpGfUc9BA"
            }
        ]
    },
    "🇪🇹 አማርኛ": {
        "ሕግና ሥርዓት": {"books": []},
        "ታሪክና ድርሳናት": {
            "ታሪክ": {"books": []},
            "ድርሳን፣ ገድልና ተአምር": {"books": []}
        },
        "ነገረ ሃይማኖት": {
            "ነገረ ቅዱሳን": {"books": []},
            "ነገረ ማርያም / ድኅነት": {"books": []},
            "ነገረ ክርስቶስ": {"books": []},
            "ነገረ ሃይማኖት": {"books": []}
        },
        "ክርስቲያናዊ ሥነ ምግባር": {"books": []},
        "የመጽሐፍ ቅዱስ ክፍል": {
            "የብሉይ ኪዳን መጻሕፍት": {"books": []},
            "የሐዲስ ኪዳን መጻሕፍት": {"books": []},
            "የመጽሐፍ ቅዱስ ጥናት": {"books": []}
        }
    },
    "🇬🇧 English": {
        "Law & Order": {"books": []},
        "History & Discourse": {
            "History": {"books": []},
            "Discourse, Hagiography & Miracles": {"books": []}
        },
        "Theology": {
            "Patristics / Saints": {"books": []},
            "Mariology / Soteriology": {"books": []},
            "Christology": {"books": []},
            "Theology": {"books": []}
        },
        "Christian Ethics": {"books": []},
        "Holy Bible Section": {
            "Old Testament Books": {"books": []},
            "New Testament Books": {"books": []},
            "Bible Study": {"books": []}
        }
    }
}

# ==========================================
# 4. OCR HELPER
# ==========================================

def is_bank_receipt(image_path: str) -> bool:
    try:
        text = pytesseract.image_to_string(Image.open(image_path)).lower()
        keywords = ["cbe", "telebirr", "bank", "transfer", "transaction", "ref", "account", "receipt", "deposited", "ebirr", "boa", "dashen"]
        return any(k in text for k in keywords)
    except Exception as e:
        print(f"OCR Error: {e}")
        return False

def get_book_by_id(data, book_id):
    if isinstance(data, dict):
        if "books" in data:
            for b in data["books"]:
                if b.get("id") == book_id:
                    return b
        for k, v in data.items():
            if k != "books":
                res = get_book_by_id(v, book_id)
                if res:
                    return res
    return None

# ==========================================
# 5. USER HANDLERS & NAVIGATION LOGIC
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_user_approved(user_id):
        msg = (
            "⚠️ አገልግሎቱን ለማግኘት አስቀድመው የባንክ ደረሰኝ (Bank Receipt) መላክ አለብዎት።\n"
            "እባክዎን የከፈሉበትን ደረሰኝ ፎቶ አሁኑኑ ይላኩ።\n\n"
            "⚠️ To access the books, please upload your Bank Receipt photo first."
        )
        await update.message.reply_text(msg)
        return

    keyboard = []
    for lang in MENU_STRUCTURE.keys():
        keyboard.append([InlineKeyboardButton(lang, callback_data=f"nav|{lang}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 **መንፈሳዊ መጽሐፍት**\nእባክዎን ቋንቋ ወይም ክፍል ይምረጡ / Choose section:", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data

    if data.startswith("book|"):
        book_id = data.split("|")[1]
        book = get_book_by_id(MENU_STRUCTURE, book_id)
        if book and book.get("file_id") and book["file_id"] != "FILE_ID_HERE":
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=book["file_id"],
                caption=f"📖 **{book['title']}**"
            )
        else:
            await query.message.reply_text("⚠️ ፋይሉ ገና ወደ ቦቱ አልተጫነም (File ID is missing).")
        return

    if data.startswith("nav|"):
        path = data.split("|")[1:]
        
        curr = MENU_STRUCTURE
        for step in path:
            curr = curr[step]

        if isinstance(curr, dict) and "books" in curr:
            books = curr["books"]
            if not books:
                is_english = path[0] == "🇬🇧 English"
                empty_msg = "(No books added to this section yet)" if is_english else "⚠️ በዚህ ክፍል እስካሁን የገቡ መጽሐፍት የሉም።"
                
                parent_path = "|".join(path[:-1])
                back_cb = f"nav|{parent_path}" if parent_path else "main"
                kb = [[InlineKeyboardButton("🔙 ወደ ኋላ (Back)", callback_data=back_cb)]]
                await query.edit_message_text(text=empty_msg, reply_markup=InlineKeyboardMarkup(kb))
                return
            
            keyboard = []
            for b in books:
                keyboard.append([InlineKeyboardButton(f"📖 {b['title']}", callback_data=f"book|{b['id']}")])
            
            parent_path = "|".join(path[:-1])
            back_cb = f"nav|{parent_path}" if parent_path else "main"
            keyboard.append([InlineKeyboardButton("🔙 ወደ ኋላ (Back)", callback_data=back_cb)])
            
            await query.edit_message_text(
                text=f"📚 **{path[-1]}** - የሚፈልጉትን መጽሐፍ ይምረጡ፡",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            return

        if isinstance(curr, dict):
            keyboard = []
            for sub_key in curr.keys():
                new_path = "|".join(path + [sub_key])
                keyboard.append([InlineKeyboardButton(sub_key, callback_data=f"nav|{new_path}")])
            
            parent_path = "|".join(path[:-1])
            back_cb = f"nav|{parent_path}" if parent_path else "main"
            keyboard.append([InlineKeyboardButton("🔙 ወደ ኋላ (Back)", callback_data=back_cb)])
            
            await query.edit_message_text(
                text=f"📂 **{path[-1]}** - ክፍል ይምረጡ፡",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            return

    if data == "main":
        keyboard = []
        for lang in MENU_STRUCTURE.keys():
            keyboard.append([InlineKeyboardButton(lang, callback_data=f"nav|{lang}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 **መንፈሳዊ መጽሐፍት**\nእባክዎን ቋንቋ ወይም ክፍል ይምረጡ / Choose section:", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"receipt_{user.id}.jpg"
    await photo_file.download_to_drive(file_path)

    if not is_bank_receipt(file_path):
        try:
            await update.message.delete()
        except Exception:
            pass
        
        warning_msg = (
            "❌ ይህ የባንክ ደረሰኝ (Bank Receipt) አይደለም! እባክዎን ትክክለኛ የባንክ ደረሰኝ ያስገቡ።\n\n"
            "❌ This is NOT a valid bank receipt! Please upload a correct bank receipt."
        )
        await context.bot.send_message(chat_id=user.id, text=warning_msg)
        if os.path.exists(file_path):
            os.remove(file_path)
        return

    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ])
    
    username_str = f"@{user.username}" if user.username else "የለውም"
    
    with open(file_path, 'rb') as photo:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=photo,
            caption=(
                f"📥 **አዲስ የክፍያ ደረሰኝ ተልኳል**\n\n"
                f"👤 **ተጠቃሚ:** {user.full_name}\n"
                f"🆔 **ID:** `{user.id}`\n"
                f"🔗 **Username:** {username_str}"
            ),
            reply_markup=admin_keyboard,
            parse_mode="Markdown"
        )

    wait_msg = (
        "✅ ደረሰኝዎ ደርሶናል! የቦቱ ባለቤት አረጋግጦ (Approve አድርጎ) እስኪያጠናቅቅ ድረስ በአክብሮት እንድትጠብቁ እንጠይቃለን።\n\n"
        "✅ We have received your receipt! Please wait respectfully until the admin approves your payment."
    )
    await update.message.reply_text(wait_msg)
    
    if os.path.exists(file_path):
        os.remove(file_path)

# ==========================================
# 6. ADMIN HANDLERS (Approve / Reject / Broadcast)
# ==========================================

async def handle_admin_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_CHAT_ID:
        return

    data = query.data
    action, user_id_str = data.split("_")
    user_id = int(user_id_str)

    if action == "approve":
        user_info = await context.bot.get_chat(user_id)
        add_approved_user(user_id, user_info.username or "", user_info.full_name or "")
        
        user_msg = (
            "🎉 ክፍያዎ በቦቱ ባለቤት ጸድቋል (Approve ተደርጓል)! አሁን ቦቱን ሙሉ ለሙሉ መጠቀም ይችላሉ።\n"
            "ወደፊት አዳዲስ መጽሐፍት ሲጨመሩ ያለምንም ተጨማሪ ክፍያ ማግኘት ይችላሉ።\n"
            "ለመጀመር /start ን ይጫኑ።\n\n"
            "🎉 Your payment has been approved! Press /start to begin using the bot."
        )
        await context.bot.send_message(chat_id=user_id, text=user_msg)
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **APPROVED (ተቀብለውታል)**")

    elif action == "reject":
        user_msg = (
            "❌ የቀረበው ደረሰኝ ውድቅ ተደርጓል (Rejected)።\n"
            "እባክዎን ትክክለኛ የባንክ ደረሰኝ እንደገና ይላኩ።\n\n"
            "❌ Your receipt was rejected. Please upload a valid bank receipt again."
        )
        await context.bot.send_message(chat_id=user_id, text=user_msg)
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **REJECTED (ውድቅ ተደርጓል)**")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        return

    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("⚠️ እባክዎን የሚላከውን መልእክት ያስገቡ። ምሳሌ፦ `/broadcast አዲስ መጽሐፍ ተጨምሯል!`")
        return

    users = get_all_approved_users()
    count = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 **ማሳወቂያ / Notification:**\n\n{message}")
            count += 1
        except Exception:
            pass

    await update.message.reply_text(f"✅ መልእክቱ ለ {count} ተጠቃሚዎች ተልኳል።")

async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        return
    users = get_all_approved_users()
    await update.message.reply_text(f"📊 **የተመዘገቡ የከፈሉ ተጠቃሚዎች ብዛት፦** {len(users)}")

async def manual_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID or not context.args:
        return
    target_id = int(context.args[0])
    add_approved_user(target_id, "", "Manual Approved")
    await update.message.reply_text(f"✅ ተጠቃሚ ID {target_id} ጸድቋል።")

async def manual_revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID or not context.args:
        return
    target_id = int(context.args[0])
    remove_approved_user(target_id)
    await update.message.reply_text(f"🚫 ተጠቃሚ ID {target_id} ፈቃዱ ተነስቷል።")

# ==========================================
# 7. MAIN RUNNER
# ==========================================

def main():
    init_db()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_message))
    app.add_handler(CommandHandler("stats", get_stats))
    app.add_handler(CommandHandler("approve_user", manual_approve))
    app.add_handler(CommandHandler("revoke_user", manual_revoke))
    
    # Callback Handlers
    app.add_handler(CallbackQueryHandler(handle_admin_decision, pattern="^(approve|reject)_"))
    app.add_handler(CallbackQueryHandler(handle_navigation))
    
    # Receipts Handler
    app.add_handler(MessageHandler(filters.PHOTO, handle_receipt))

    print("🚀 ቦቱ በስኬት ስራ ጀምሯል...")
    app.run_polling()

if __name__ == "__main__":
    main()