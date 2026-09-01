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
# 1. CONFIGURATION
# ==========================================

ADMIN_CHAT_ID = 123456789  # ⚠️ የቦቱ ባለቤት Telegram Chat ID እዚህ ይተኩ
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # ⚠️ የቦት ቶከንዎን እዚህ ይተኩ

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
# 3. BOOKS & MENU STRUCTURE
# ከዚህ በኋላ አዳዲስ መጽሐፍ ሲኖሩ id, title እና file_id ብቻ መጨመር ነው
# ==========================================

MENU_STRUCTURE = {
    "ግእዝ": {
        "የመጽሐፍ ቅዱስ ክፍል": {
            "books": [
                {"id": "gz_b1", "title": "ኦሪት ዘፍጥረት (ግእዝ)", "file_id": "FILE_ID_HERE"},
                {"id": "gz_b2", "title": "ወንጌል ዘማቴዎስ (ግእዝ)", "file_id": "FILE_ID_HERE"}
            ]
        }
    },
    "ግእዝ-አማርኛ": {
        "የመጽሐፍ ቅዱስ ክፍል": {
            "books": [
                {"id": "ga_b1", "title": "መጽሐፈ ሄኖክ (ግእዝ-አማርኛ)", "file_id": "FILE_ID_HERE"}
            ]
        }
    },
    "አማርኛ": {
        "የመጽሐፍ ቅዱስ ክፍል": {
            "books": [
                {"id": "am_b1", "title": "የመጽሐፍ ቅዱስ ጥናት", "file_id": "FILE_ID_HERE"}
            ]
        },
        "ነገረ ሃይማኖት": {
            "ነገረ ማርያም / ድኅነት": {
                "books": [
                    {"id": "am_m1", "title": "ነገረ ማርያም በቤተክርስቲያን ታሪክ", "file_id": "FILE_ID_HERE"}
                ]
            }
        },
        "ክርስቲያናዊ ሥነ ምግባር": {
            "books": [
                {"id": "am_e1", "title": "ክርስቲያናዊ ሕይወት", "file_id": "FILE_ID_HERE"}
            ]
        }
    },
    "English": {
        "Bible Section": {
            "books": [
                {"id": "en_b1", "title": "Holy Bible (KJV)", "file_id": "FILE_ID_HERE"}
            ]
        },
        "Systematic Theology": {
            "Mariology / Salvation": {
                "books": [
                    {"id": "en_m1", "title": "Dogmatic Theology", "file_id": "FILE_ID_HERE"}
                ]
            }
        },
        "Christian Ethics": {
            "books": [
                {"id": "en_e1", "title": "Christian Life & Ethics", "file_id": "FILE_ID_HERE"}
            ]
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
    except Exception:
        return False

# ==========================================
# 5. USER HANDLERS
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

    # ፈቃድ ያላቸው ተጠቃሚዎች ዋና ሜኑ ያያሉ
    keyboard = [[InlineKeyboardButton(lang, callback_data=f"main_{lang}")] for lang in MENU_STRUCTURE.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("እንኳን ደህና መጡ! እባክዎን ቋንቋ ወይም ክፍል ይምረጡ፡ / Choose section:", reply_markup=reply_markup)

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"receipt_{user.id}.jpg"
    await photo_file.download_to_drive(file_path)

    # ደረሰኝ መሆኑን ማረጋገጥ
    if not is_bank_receipt(file_path):
        await update.message.delete()  # አውቶማቲክ ስረዛ
        
        warning_msg = (
            "❌ ይህ የባንክ ደረሰኝ (Bank Receipt) አይደለም! እባክዎን ትክክለኛ የባንክ ደረሰኝ ያስገቡ።\n\n"
            "❌ This is NOT a valid bank receipt! Please upload a correct bank receipt."
        )
        await context.bot.send_message(chat_id=user.id, text=warning_msg)
        if os.path.exists(file_path):
            os.remove(file_path)
        return

    # ትክክለኛ ከሆነ ለአድሚን መላክ
    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ])
    
    username_str = f"@{user.username}" if user.username else "የለውም"
    await context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=open(file_path, 'rb'),
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
        # ተጠቃሚውን በ SQLite መመዝገብ
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
    """ለቀደሙት ተጠቃሚዎች በሙሉ መልእክት መላኪያ (/broadcast <message>)"""
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
            pass  # ተጠቃሚው ቦቱን Block አድርጎት ከሆነ ይዘለላል

    await update.message.reply_text(f"✅ መልእክቱ ለ {count} ተጠቃሚዎች ተልኳል።")

async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """የተመዘገቡ ተጠቃሚዎች ብዛት ማየቻ (/stats)"""
    if update.effective_user.id != ADMIN_CHAT_ID:
        return
    users = get_all_approved_users()
    await update.message.reply_text(f"📊 **የተመዘገቡ የከፈሉ ተጠቃሚዎች ብዛት፦** {len(users)}")

async def manual_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """በቤት ባለቤት በ ID ፈቃድ መስጫ (/approve_user <id>)"""
    if update.effective_user.id != ADMIN_CHAT_ID or not context.args:
        return
    target_id = int(context.args[0])
    add_approved_user(target_id, "", "Manual Approved")
    await update.message.reply_text(f"✅ ተጠቃሚ ID {target_id} ጸድቋል።")

async def manual_revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """በቤት ባለቤት በ ID ፈቃድ መንሻ (/revoke_user <id>)"""
    if update.effective_user.id != ADMIN_CHAT_ID or not context.args:
        return
    target_id = int(context.args[0])
    remove_approved_user(target_id)
    await update.message.reply_text(f"🚫 ተጠቃሚ ID {target_id} ፈቃዱ ተነስቷል።")

# ==========================================
# 7. MAIN RUNNER
# ==========================================

def main():
    init_db()  # ዳታቤዝ ማስጀመር
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_message))
    app.add_handler(CommandHandler("stats", get_stats))
    app.add_handler(CommandHandler("approve_user", manual_approve))
    app.add_handler(CommandHandler("revoke_user", manual_revoke))
    
    app.add_handler(MessageHandler(filters.PHOTO, handle_receipt))
    app.add_handler(CallbackQueryHandler(handle_admin_decision, pattern="^(approve|reject)_"))

    print("🚀 ቦቱ በስኬት ስራ ጀምሯል...")
    app.run_polling()

if __name__ == "__main__":
    main()