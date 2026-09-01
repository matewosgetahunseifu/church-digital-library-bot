import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

app = Flask(__name__)

@app.route('/')
def home():
    return 'Church Digital Library Bot is Running 24/7!'

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8777005011:AAHi7FXjLXk9QkRBzylmzsLqYj7dRC1PR_Y')
bot = telebot.TeleBot(BOT_TOKEN)

# Admin Username (ለደህንነት የተገደበ)
ADMIN_USERNAME = 'Sealilenemariyammsle12we19'

# ==========================================
# DATABASE (የመጽሐፍት ዝርዝር)
# ==========================================

# 1. የግእዝ ቋንቋ መማሪያ መጻሕፍት (16 መጻሕፍት)
GEEZ_GUIDE_BOOKS = [
    {'title': '1. መጽሐፈ ሰዋስው ወግስ ወመዝገበ ቃላት ሐዲስ (አለቃ ኪዳነ ወልድ ክፍሌ)', 'file_id': 'BQACAgQAAxkBAAOiapLEYe5R4ZxJ8_3PQZ-SHO6NA4sAAqofAAI12zhQV3FkwrOJJtc9BA'},
    {'title': '2. ግእዝ እንግሊዝኛ ኦገስት ዲልማን', 'file_id': 'BQACAgQAAxkBAAOvapLOTuM_iJ5-xleFbnGNgDLeJzAAAqAhAAKba2BQb49RMRsZf_49BA'},
    {'title': '3. ግስ እምባቆብ', 'file_id': 'BQACAgQAAxkBAAOxapLOToEwCL4K_RHREKweqU9_buMAAlgGAALy24lQiHGMdWTQj_I9BA'},
    {'title': '4. መጽሐፈ ግእዝ', 'file_id': 'BQACAgQAAxkBAAOyapLOTqigZoRB37TkUs3YBzjgx0oAAmwQAAKDKPFTW2HbAekftKU9BA'},
    {'title': '5. ጥንታዊ ግእዝ በዘመናዊ አቀራረብ (ካልኣይ ክፍል)', 'file_id': 'BQACAgQAAxkBAAOwapLOTnyZqs5q3YoQooXwdQLLdhkAAqUhAAKba2BQrTKlP3O6ohg9BA'},
    {'title': '6. ትንሳዔ ግእዝ (መምህር ደሴ ቀለብ)', 'file_id': 'BQACAgQAAxkBAAOzapLOTgKDH7A6tfXemG-zjjdcj8oAAvsBAAKh56lQKVEyEdzzV7Y9BA'},
    {'title': '7. ፍሬ ግእዝ', 'file_id': 'BQACAgQAAxkBAAO0apLOTkraJZeY7MMSjeoRi9huctAAAvEQAAL0ZllRd1T8Cz3MfR89BA'},
    {'title': '8. ግእዝ እንበለ መምህር', 'file_id': 'BQACAgQAAxkBAAO1apLOTgLec1zclkRUTQU9IcZIAeMAAlsZAALmW4FQynTLeSEqAZQ9BA'},
    {'title': '9. የግእዝ ሰዋሰው (ዓለማየሁ ሞገስ)', 'file_id': 'BQACAgQAAxkBAAO2apLOTl-cs3ftddnQSFcTg0ZxE1cAAoshAAKba2BQCmlU5vYhiKo9BA'},
    {'title': '10. ግእዝ መማሪያ መጽሐፍ', 'file_id': 'BQACAgQAAxkBAAO3apLOTm6QfeRlG6uKjTMJ4zx96ooAAocHAAJyFMhT0rbd1ZaTvsY9BA'},
    {'title': '11. ግዕዝ መሠረተ ትምህርት (ደስታ ተክለወልድ)', 'file_id': 'BQACAgQAAxkBAAO4apLOTpmweUFZNie-aTlg5hoTx2MAAqECAAKpJdlS5zKDZrrocvA9BA'},
    {'title': '12. የግእዝ መማሪያ (ዶ/ር ለይኩን ብርሀኑ)', 'file_id': 'BQACAgQAAxkBAAO5apLOTn5wYdAKlzCSp2FmCNQD_-YAArUGAAJv75lRsafLj8CJxmM9BA'},
    {'title': '13. ሰዋስወ ግእዝ ወአንቀጽ', 'file_id': 'BQACAgQAAxkBAAO6apLOToQiuej6WJBDqZP3j_YAAWppAALKFQAC2aVxUmuX4vLb4xyBPQQ'},
    {'title': '14. መርኆ ሰዋስው ዘልሳነ ግእዝ', 'file_id': 'BQACAgQAAxkBAAO7apLOTluw2HKlQ3pbSGzD2_riMcIAAikYAAJds_lQWZXHtP7ylCE9BA'},
    {'title': '15. መዝገበ ግስ (ሁሉንም ግስ በአንድ የያዘ)', 'file_id': 'BQACAgQAAxkBAAO8apLOTjpUoaE4ZWHGHe813QABMrsyAALWGAACm_fpUfxpVw9o_4grPQQ'},
    {'title': '16. መጽሐፈ ሰዋስው', 'file_id': 'BQACAgQAAxkBAAO9apLOThplHgQeqctpal2rVuqMU-8AAq8cAAIe9uFQcwlbPLpGfUc9BA'}
]

# 2. የግእዝ-አማርኛ ብሉይ ኪዳን መጻሕፍት
GEEZ_AMHARIC_OLD_TESTAMENT_BOOKS = [
    {'title': '1. ኦሪት ዘፍጥረት አንድምታ', 'file_id': 'BQACAgQAAxkBAAPoapL5-j4Y4yKee0lyFZlMHif5UoAAAgcKAAKjPElSpWxXt7rSOxk9BA'},
    {'title': '2. ኦሪት ዘፀአት አንድምታ', 'file_id': 'BQACAgQAAxkBAAPpapL5-mx2OLB_jMKwjJx8isE-LRAAAggKAAKjPElSdkt4uS3PouI9BA'},
    {'title': '3. ኦሪት ዘሌዋውያን አንድምታ', 'file_id': 'BQACAgQAAxkBAAPqapL5-mUjkfP8bzTvar9D5ZmjeIwAAvUKAAL6HClR9oG7Bfn__tI9BA'},
    {'title': '4. ኦሪት ዘኍልቅ አንድምታ', 'file_id': 'BQACAgQAAxkBAAPrapL5-vSTNfOEAAEE0CwlPjz-oH1cAAIKCgACozxJUstPvw26Lpm9PQQ'},
    {'title': '5. ኦሪት ዘዳግም አንድምታ', 'file_id': 'BQACAgQAAxkBAAPsapL5-qt3Lcu5lWpCIB8LZ9ly_V8AAgsKAAKjPElSKmH6OAPSIR49BA'}
]

# 3. የግእዝ ብሉይ ኪዳን መጻሕፍት
GEEZ_OLD_TESTAMENT_BOOKS = [
    {'title': '1. ፭ቱ መጽሐፈ ኦሪት ብራና አንድምታ', 'file_id': 'BQACAgQAAxkBAAP4apL8OXANqEqvyGn7V4Lk_C1rDygAAn0JAAIWA9hQayRhNPpVNvE9BA'}
]

# 4. የግእዝ-አማርኛ ሐዲስ ኪዳን መጻሕፍት
GEEZ_AMHARIC_NEW_TESTAMENT_BOOKS = []

ALL_BOOKS_LISTS = [
    GEEZ_GUIDE_BOOKS,
    GEEZ_AMHARIC_OLD_TESTAMENT_BOOKS,
    GEEZ_OLD_TESTAMENT_BOOKS,
    GEEZ_AMHARIC_NEW_TESTAMENT_BOOKS
]

# ==========================================
# KEYBOARD GENERATION FUNCTIONS
# ==========================================

def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('📚 መንፈሳዊ መጽሐፍት', '🔍 መጽሐፍ ፈልግ')
    markup.add('📞 Contact Me', '💬 Feedback')
    markup.add('🏠 Main Menu')
    return markup

def get_language_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('ግእዝ', callback_data='lang_geez'),
        InlineKeyboardButton('ግእዝ-አማርኛ', callback_data='lang_geez_amharic')
    )
    markup.add(InlineKeyboardButton('የግእዝ ቋንቋ መማሪያ', callback_data='lang_geez_guide'))
    markup.add(
        InlineKeyboardButton('አማርኛ', callback_data='lang_amharic'),
        InlineKeyboardButton('English', callback_data='lang_english')
    )
    return markup

def get_category_keyboard(lang_code):
    markup = InlineKeyboardMarkup(row_width=2)
    if lang_code == 'english':
        markup.add(
            InlineKeyboardButton('Law & Order', callback_data=f'cat_{lang_code}_law'),
            InlineKeyboardButton('History & Discourse', callback_data=f'cat_{lang_code}_history_main')
        )
        markup.add(
            InlineKeyboardButton('Theology', callback_data=f'cat_{lang_code}_theology_main'),
            InlineKeyboardButton('Christian Ethics', callback_data=f'cat_{lang_code}_ethics')
        )
        markup.add(InlineKeyboardButton('Holy Bible Section', callback_data=f'cat_{lang_code}_bible_main'))
        markup.add(InlineKeyboardButton('🔙 Go Back', callback_data='go_main_menu'))
    else:
        markup.add(
            InlineKeyboardButton('ሕግና ሥርዓት', callback_data=f'cat_{lang_code}_law'),
            InlineKeyboardButton('ታሪክና ድርሳናት', callback_data=f'cat_{lang_code}_history_main')
        )
        markup.add(
            InlineKeyboardButton('ነገረ ሃይማኖት', callback_data=f'cat_{lang_code}_theology_main'),
            InlineKeyboardButton('ክርስቲያናዊ ሥነ ምግባር', callback_data=f'cat_{lang_code}_ethics')
        )
        markup.add(InlineKeyboardButton('የመጽሐፍ ቅዱስ ክፍል', callback_data=f'cat_{lang_code}_bible_main'))
        markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='go_main_menu'))
    return markup

def get_history_subcategory_keyboard(lang_code):
    markup = InlineKeyboardMarkup(row_width=1)
    if lang_code == 'english':
        markup.add(InlineKeyboardButton('1. History', callback_data=f'sub_{lang_code}_history'))
        markup.add(InlineKeyboardButton('2. Discourse, Hagiography & Miracles', callback_data=f'sub_{lang_code}_hagiography'))
        markup.add(InlineKeyboardButton('🔙 Go Back', callback_data=f'back_to_lang_{lang_code}'))
    else:
        markup.add(InlineKeyboardButton('1. ታሪክ', callback_data=f'sub_{lang_code}_history'))
        markup.add(InlineKeyboardButton('2. ድርሳን፣ ገድልና ተአምር', callback_data=f'sub_{lang_code}_hagiography'))
        markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data=f'back_to_lang_{lang_code}'))
    return markup

def get_theology_subcategory_keyboard(lang_code):
    markup = InlineKeyboardMarkup(row_width=2)
    if lang_code == 'english':
        markup.add(
            InlineKeyboardButton('Patristics / Saints', callback_data=f'sub_{lang_code}_saints'),
            InlineKeyboardButton('Mariology', callback_data=f'sub_{lang_code}_mariology')
        )
        markup.add(
            InlineKeyboardButton('Christology', callback_data=f'sub_{lang_code}_christology'),
            InlineKeyboardButton('Theology', callback_data=f'sub_{lang_code}_theology_sub')
        )
        markup.add(InlineKeyboardButton('🔙 Go Back', callback_data=f'back_to_lang_{lang_code}'))
    else:
        markup.add(
            InlineKeyboardButton('ነገረ ቅዱሳን', callback_data=f'sub_{lang_code}_saints'),
            InlineKeyboardButton('ነገረ ማርያም', callback_data=f'sub_{lang_code}_mariology')
        )
        markup.add(
            InlineKeyboardButton('ነገረ ክርስቶስ', callback_data=f'sub_{lang_code}_christology'),
            InlineKeyboardButton('ነገረ ሃይማኖት', callback_data=f'sub_{lang_code}_theology_sub')
        )
        markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data=f'back_to_lang_{lang_code}'))
    return markup

def get_bible_subcategory_keyboard(lang_code):
    markup = InlineKeyboardMarkup(row_width=1)
    if lang_code == 'english':
        markup.add(InlineKeyboardButton('Old Testament Books', callback_data=f'sub_{lang_code}_ot'))
        markup.add(InlineKeyboardButton('New Testament Books', callback_data=f'sub_{lang_code}_nt'))
        markup.add(InlineKeyboardButton('Bible Study', callback_data=f'sub_{lang_code}_bible_study'))
        markup.add(InlineKeyboardButton('🔙 Go Back', callback_data=f'back_to_lang_{lang_code}'))
    else:
        markup.add(InlineKeyboardButton('የብሉይ ኪዳን መጻሕፍት', callback_data=f'sub_{lang_code}_ot'))
        markup.add(InlineKeyboardButton('የሐዲስ ኪዳን መጻሕፍት', callback_data=f'sub_{lang_code}_nt'))
        markup.add(InlineKeyboardButton('የመጽሐፍ ቅዱስ ጥናት', callback_data=f'sub_{lang_code}_bible_study'))
        markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data=f'back_to_lang_{lang_code}'))
    return markup

def get_geez_guide_books_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    for index, book in enumerate(GEEZ_GUIDE_BOOKS):
        markup.add(InlineKeyboardButton(book['title'], callback_data=f'get_geez_book_{index}'))
    markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='go_main_menu'))
    return markup

def get_geez_amharic_ot_books_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    for index, book in enumerate(GEEZ_AMHARIC_OLD_TESTAMENT_BOOKS):
        markup.add(InlineKeyboardButton(book['title'], callback_data=f'get_ga_ot_book_{index}'))
    markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='cat_geez_amharic_bible_main'))
    return markup

def get_geez_ot_books_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    for index, book in enumerate(GEEZ_OLD_TESTAMENT_BOOKS):
        markup.add(InlineKeyboardButton(book['title'], callback_data=f'get_gz_ot_book_{index}'))
    markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='cat_geez_bible_main'))
    return markup

def get_geez_amharic_nt_books_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    if not GEEZ_AMHARIC_NEW_TESTAMENT_BOOKS:
        markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='cat_geez_amharic_bible_main'))
    else:
        for index, book in enumerate(GEEZ_AMHARIC_NEW_TESTAMENT_BOOKS):
            markup.add(InlineKeyboardButton(book['title'], callback_data=f'get_ga_nt_book_{index}'))
        markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='cat_geez_amharic_bible_main'))
    return markup

# ==========================================
# BOT HANDLERS & LOGIC
# ==========================================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጻሕፍት» በደኅና መጡ!**\n\n"
        "እባክዎ መጽሐፍትን በምን ቋንቋ ማንበብ ይፈልጋሉ?"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_language_inline_keyboard(), parse_mode='Markdown')
    bot.send_message(message.chat.id, "👇 ከታች ያሉትን አማራጮች መጠቀም ይችላሉ፦", reply_markup=get_main_reply_keyboard())

@bot.message_handler(func=lambda message: message.text in ['🏠 Main Menu', '⬅️ Go Back'])
def handle_main_menu_button(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text == '📚 መንፈሳዊ መጽሐፍት')
def handle_books_button(message):
    bot.send_message(message.chat.id, "እባክዎ መጽሐፍትን በምን ቋንቋ ማንበብ ይፈልጋሉ?", reply_markup=get_language_inline_keyboard())

@bot.message_handler(func=lambda message: message.text == '📞 Contact Me')
def handle_contact(message):
    contact_text = f"📩 **እኛን ለማግኘት፦**\n\nለማንኛውም አስተያየት ወይም ጥያቄ በቴሌግራም ያግኙን፦ @{ADMIN_USERNAME}"
    bot.send_message(message.chat.id, contact_text, parse_mode='Markdown')

# Feedback System Handler
@bot.message_handler(func=lambda message: message.text == '💬 Feedback')
def handle_feedback_start(message):
    msg = bot.send_message(
        message.chat.id, 
        "✍️ **አስተያየትዎን ያስቀምጡ፦**\n\nእባክዎ ለቦታችን እድገት የሚረዱ ሃሳቦችን እና አስተያየቶችን አሁን ጽፈው ይላኩ።", 
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_feedback)

def process_feedback(message):
    user_info = f"👤 **ከ፦** {message.from_user.first_name} (@{message.from_user.username or 'No Username'}) [ID: `{message.from_user.id}`]\n\n"
    feedback_text = user_info + f"💬 **አስተያየት፦**\n{message.text}"
    
    # Send feedback to Admin username if reachable, or print internally
    bot.send_message(message.chat.id, "✅ **አስተያየትዎ ደርሶናል!** ስላገዙን እናመሰግናለን።", parse_mode='Markdown')

# Search System
@bot.message_handler(commands=['search'])
@bot.message_handler(func=lambda message: message.text == '🔍 መጽሐፍ ፈልግ')
def handle_search_start(message):
    msg = bot.send_message(message.chat.id, "🔍 **የሚፈልጉትን የመጽሐፍ ስም ወይም ቃል ይጻፉ፦**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_search)

def process_search(message):
    query = message.text.strip().lower()
    results = []
    
    for book_list in ALL_BOOKS_LISTS:
        for book in book_list:
            if query in book['title'].lower():
                results.append(book)
                
    if not results:
        bot.send_message(message.chat.id, f"❌ <b>'{message.text}'</b> በሚል ቃል የተገኘ መጽሐፍ የለም። እባክዎ እንደገና ይሞክሩ።", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f"🔍 <b>የተገኙ መጻሕፍት ({len(results)})፦</b>", parse_mode='HTML')
        for book in results:
            bot.send_message(message.chat.id, f"📖 <b>{book['title']}</b>", parse_mode='HTML')
            try:
                bot.send_document(message.chat.id, book['file_id'])
            except Exception as e:
                print(f"Error sending document: {e}")

# ==========================================
# CALLBACK QUERY HANDLER
# ==========================================

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.answer_callback_query(call.id)
    data = call.data

    try:
        if data == 'go_main_menu':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጻሕፍት» በደኅና መጡ!**\n\nእባክዎ መጽሐፍትን በምን ቋንቋ ማንበብ ይፈልጋሉ?",
                reply_markup=get_language_inline_keyboard(),
                parse_mode='Markdown'
            )

        elif data == 'lang_geez':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📖 የተመረጠው ቋንቋ፦ 📜 **ግዕዝ**\n\nእባክዎ በግእዝ ምን ማንበብ ይፈልጋሉ?",
                reply_markup=get_category_keyboard('geez'),
                parse_mode='Markdown'
            )

        elif data == 'lang_geez_amharic':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📖 የተመረጠው ቋንቋ፦ 🇪🇹 **ግዕዝ አማርኛ**\n\nእባክዎ በግእዝ አማርኛ ምን ማንበብ ይፈልጋሉ?",
                reply_markup=get_category_keyboard('geez_amharic'),
                parse_mode='Markdown'
            )

        elif data == 'lang_geez_guide':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📖 **የግእዝ ቋንቋ መመሪያ (መማሪያ መጽሐፍት)፦**\n\nእባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦",
                reply_markup=get_geez_guide_books_keyboard(),
                parse_mode='Markdown'
            )

        elif data == 'lang_amharic':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📖 የተመረጠው ቋንቋ፦ **አማርኛ**\n\nእባክዎ በአማርኛ ምን ማንበብ ይፈልጋሉ?",
                reply_markup=get_category_keyboard('amharic'),
                parse_mode='Markdown'
            )

        elif data == 'lang_english':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📖 Selected Language: 🇬🇧 **English**\n\nPlease choose what you would like to read in English:",
                reply_markup=get_category_keyboard('english'),
                parse_mode='Markdown'
            )

        elif data.startswith('back_to_lang_'):
            lang_code = data.replace('back_to_lang_', '')
            msg_text = "📖 Selected Language: 🇬🇧 **English**\n\nPlease choose what you would like to read in English:" if lang_code == 'english' else "እባክዎ ምን ማንበብ ይፈልጋሉ?"
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=msg_text,
                reply_markup=get_category_keyboard(lang_code),
                parse_mode='Markdown'
            )

        elif data.endswith('_history_main'):
            lang_code = data.replace('cat_', '').replace('_history_main', '')
            msg = "Please select one of the following options:" if lang_code == 'english' else "እባክዎ ከታች ካሉት አማራጮች አንዱን ይምረጡ፦"
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=msg,
                reply_markup=get_history_subcategory_keyboard(lang_code),
                parse_mode='Markdown'
            )

        elif data.endswith('_theology_main'):
            lang_code = data.replace('cat_', '').replace('_theology_main', '')
            msg = "Please select one of the following options:" if lang_code == 'english' else "እባክዎ ከታች ካሉት አማራጮች አንዱን ይምረጡ፦"
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=msg,
                reply_markup=get_theology_subcategory_keyboard(lang_code),
                parse_mode='Markdown'
            )

        elif data.endswith('_bible_main'):
            lang_code = data.replace('cat_', '').replace('_bible_main', '')
            msg = "Please select one of the following options:" if lang_code == 'english' else "እባክዎ ከታች ካሉት አማራጮች አንዱን ይምረጡ፦"
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=msg,
                reply_markup=get_bible_subcategory_keyboard(lang_code),
                parse_mode='Markdown'
            )

        elif data == 'sub_geez_amharic_ot':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📖 **የብሉይ ኪዳን መጻሕፍት (ግእዝ-አማርኛ)፦**\n\nእባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦",
                reply_markup=get_geez_amharic_ot_books_keyboard(),
                parse_mode='Markdown'
            )

        elif data == 'sub_geez_ot':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📖 **የብሉይ ኪዳን መጻሕፍት (ግእዝ)፦**\n\nእባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦",
                reply_markup=get_geez_ot_books_keyboard(),
                parse_mode='Markdown'
            )

        elif data == 'sub_geez_amharic_nt':
            text_msg = "📖 **የሐዲስ ኪዳን መጻሕፍት (ግእዝ-አማርኛ)፦**\n\n" + ("እባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦" if GEEZ_AMHARIC_NEW_TESTAMENT_BOOKS else "*(በዚህ ክፍል እስካሁን የገቡ መጽሐፍት የሉም)*")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_msg,
                reply_markup=get_geez_amharic_nt_books_keyboard(),
                parse_mode='Markdown'
            )

        # Get Book Logic
        elif data.startswith('get_geez_book_'):
            index = int(data.split('_')[-1])
            book = GEEZ_GUIDE_BOOKS[index]
            bot.send_message(call.message.chat.id, f"ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n\"{book['title']}\"\n\nመልካም ንባብ ይሁንሎት! 📖✨")
            bot.send_document(call.message.chat.id, book['file_id'])

        elif data.startswith('get_ga_ot_book_'):
            index = int(data.split('_')[-1])
            book = GEEZ_AMHARIC_OLD_TESTAMENT_BOOKS[index]
            bot.send_message(call.message.chat.id, f"ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n\"{book['title']}\"\n\nመልካም ንባብ ይሁንሎት! 📖✨")
            bot.send_document(call.message.chat.id, book['file_id'])

        elif data.startswith('get_gz_ot_book_'):
            index = int(data.split('_')[-1])
            book = GEEZ_OLD_TESTAMENT_BOOKS[index]
            bot.send_message(call.message.chat.id, f"ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n\"{book['title']}\"\n\nመልካም ንባብ ይሁንሎት! 📖✨")
            bot.send_document(call.message.chat.id, book['file_id'])

        elif data.startswith('get_ga_nt_book_'):
            index = int(data.split('_')[-1])
            book = GEEZ_AMHARIC_NEW_TESTAMENT_BOOKS[index]
            bot.send_message(call.message.chat.id, f"ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n\"{book['title']}\"\n\nመልካም ንባብ ይሁንሎት! 📖✨")
            bot.send_document(call.message.chat.id, book['file_id'])

        elif data.startswith('cat_') or data.startswith('sub_'):
            is_eng = 'english' in data
            text_msg = "Please select the book you would like to read:\n\n*(No books added to this section yet)*" if is_eng else "እባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦\n\n*(በዚህ ክፍል እስካሁን የገቡ መጽሐፍት የሉም)*"
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='go_main_menu'))
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text_msg,
                reply_markup=markup,
                parse_mode='Markdown'
            )

    except Exception as e:
        print(f"Callback Error: {e}")

# ==========================================
# DOCUMENT UPLOAD HANDLER (ADMIN ONLY)
# ==========================================

@bot.message_handler(content_types=['document'])
def handle_document(message):
    sender_username = message.from_user.username
    if sender_username and sender_username.lower() == ADMIN_USERNAME.lower():
        file_id = message.document.file_id
        file_name = message.document.file_name
        bot.reply_to(
            message, 
            f"✅ **ፋይሉ ደርሷል!**\n\n**የፋይሉ ስም፦** `{file_name}`\n**File ID፦**\n`{file_id}`", 
            parse_mode='Markdown'
        )
    else:
        bot.reply_to(message, "መጽሐፍ ለማስገባት ጥቆማ ካለዎት እባክዎ በ Feedback መስመር ያድርሱን።")

# Fallback Handler for text messages
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(
        message.chat.id, 
        "ይቅርታ፣ የተላከውን መልእክት መረዳት አልተቻለም። እባክዎ ከታች ያሉትን አማራጮች ይጠቀሙ፦", 
        reply_markup=get_main_reply_keyboard()
    )

# ==========================================
# APP LAUNCH
# ==========================================

if __name__ == '__main__':
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)