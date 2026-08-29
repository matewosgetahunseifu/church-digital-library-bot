import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# ----------------------------------------------------
# 1. Flask Web Server (Render Keep-Alive)
# ----------------------------------------------------
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


# ----------------------------------------------------
# 2. Telegram Bot Configuration
# ----------------------------------------------------
BOT_TOKEN = os.environ.get(
    'BOT_TOKEN', '8777005011:AAHi7FXjLXk9QkRBzylmzsLqYj7dRC1PR_Y'
)
bot = telebot.TeleBot(BOT_TOKEN)

# የአንተ የቴሌግራም Username (ለደህንነት)
ADMIN_USERNAME = 'Sealilenemariyammsle12we19'

# ----------------------------------------------------
# 3. Database (የግእዝ መማሪያ መጽሐፍት ዝርዝር)
# ----------------------------------------------------
GEEZ_BOOKS = [
    {
        'title': '1. መጽሐፈ ሰዋስው ወግስ ወመዝገበ ቃላት ሐዲስ (አለቃ ኪዳነ ወልድ ክፍሌ)',
        'file_id': (
            'BQACAgQAAxkBAAOiapLEYe5R4ZxJ8_3PQZ-SHO6NA4sAAqofAAI12zhQV3FkwrOJJtc9BA'
        ),
    },
    {
        'title': '2. ግእዝ እንግሊዝኛ ኦገስት ዲልማን',
        'file_id': (
            'BQACAgQAAxkBAAOvapLOTuM_iJ5-xleFbnGNgDLeJzAAAqAhAAKba2BQb49RMRsZf_49BA'
        ),
    },
    {
        'title': '3. ግስ እምባቆብ',
        'file_id': (
            'BQACAgQAAxkBAAOxapLOToEwCL4K_RHREKweqU9_buMAAlgGAALy24lQiHGMdWTQj_I9BA'
        ),
    },
    {
        'title': '4. መጽሐፈ ግእዝ',
        'file_id': (
            'BQACAgQAAxkBAAOyapLOTqigZoRB37TkUs3YBzjgx0oAAmwQAAKDKPFTW2HbAekftKU9BA'
        ),
    },
    {
        'title': '5. ጥንታዊ ግእዝ በዘመናዊ አቀራረብ (ካልኣይ ክፍል)',
        'file_id': (
            'BQACAgQAAxkBAAOwapLOTnyZqs5q3YoQooXwdQLLdhkAAqUhAAKba2BQrTKlP3O6ohg9BA'
        ),
    },
    {
        'title': '6. ትንሳዔ ግእዝ (መምህር ደሴ ቀለብ)',
        'file_id': (
            'BQACAgQAAxkBAAOzapLOTgKDH7A6tfXemG-zjjdcj8oAAvsBAAKh56lQKVEyEdzzV7Y9BA'
        ),
    },
    {
        'title': '7. ፍሬ ግእዝ',
        'file_id': (
            'BQACAgQAAxkBAAO0apLOTkraJZeY7MMSjeoRi9huctAAAvEQAAL0ZllRd1T8Cz3MfR89BA'
        ),
    },
    {
        'title': '8. ግእዝ እንበለ መምህር',
        'file_id': (
            'BQACAgQAAxkBAAO1apLOTgLec1zclkRUTQU9IcZIAeMAAlsZAALmW4FQynTLeSEqAZQ9BA'
        ),
    },
    {
        'title': '9. የግእዝ ሰዋሰው (ዓለማየሁ ሞገስ)',
        'file_id': (
            'BQACAgQAAxkBAAO2apLOTl-cs3ftddnQSFcTg0ZxE1cAAoshAAKba2BQCmlU5vYhiKo9BA'
        ),
    },
    {
        'title': '10. ግእዝ መማሪያ መጽሐፍ',
        'file_id': (
            'BQACAgQAAxkBAAO3apLOTm6QfeRlG6uKjTMJ4zx96ooAAocHAAJyFMhT0rbd1ZaTvsY9BA'
        ),
    },
    {
        'title': '11. ግዕዝ መሠረተ ትምህርት (ደስታ ተክለወልድ)',
        'file_id': (
            'BQACAgQAAxkBAAO4apLOTpmweUFZNie-aTlg5hoTx2MAAqECAAKpJdlS5zKDZrrocvA9BA'
        ),
    },
    {
        'title': '12. የግእዝ መማሪያ (ዶ/ር ለይኩን ብርሀኑ)',
        'file_id': (
            'BQACAgQAAxkBAAO5apLOTn5wYdAKlzCSp2FmCNQD_-YAArUGAAJv75lRsafLj8CJxmM9BA'
        ),
    },
    {
        'title': '13. ሰዋስወ ግእዝ ወአንቀጽ',
        'file_id': (
            'BQACAgQAAxkBAAO6apLOToQiuej6WJBDqZP3j_YAAWppAALKFQAC2aVxUmuX4vLb4xyBPQQ'
        ),
    },
    {
        'title': '14. መርኆ ሰዋስው ዘልሳነ ግእዝ',
        'file_id': (
            'BQACAgQAAxkBAAO7apLOTluw2HKlQ3pbSGzD2_riMcIAAikYAAJds_lQWZXHtP7ylCE9BA'
        ),
    },
    {
        'title': '15. መዝገበ ግስ (ሁሉንም ግስ በአንድ የያዘ)',
        'file_id': (
            'BQACAgQAAxkBAAO8apLOTjpUoaE4ZWHGHe813QABMrsyAALWGAACm_fpUfxpVw9o_4grPQQ'
        ),
    },
    {
        'title': '16. መጽሐፈ ሰዋስው',
        'file_id': (
            'BQACAgQAAxkBAAO9apLOThplHgQeqctpal2rVuqMU-8AAq8cAAIe9uFQcwlbPLpGfUc9BA'
        ),
    },
]

# ----------------------------------------------------
# 4. Keyboards (የቁልፎች አደረጃጀት)
# ----------------------------------------------------


def get_main_reply_keyboard():
  markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  markup.add('📚 መንፈሳዊ መጽሐፍት')
  markup.add('📞 Contact Me', '💬 Feedback')
  markup.add('🏠 Main Menu')
  return markup


def get_language_inline_keyboard():
  markup = InlineKeyboardMarkup(row_width=2)
  markup.add(
      InlineKeyboardButton('ግዕዝ መማሪያ', callback_data='lang_geez_guide'),
      InlineKeyboardButton('ግዕዝ-አማርኛ', callback_data='lang_geez_amharic'),
  )
  markup.add(
      InlineKeyboardButton('አማርኛ', callback_data='lang_amharic'),
      InlineKeyboardButton('English', callback_data='lang_english'),
  )
  return markup


def get_geez_books_keyboard():
  markup = InlineKeyboardMarkup(row_width=1)
  for index, book in enumerate(GEEZ_BOOKS):
    markup.add(
        InlineKeyboardButton(
            book['title'], callback_data=f'get_geez_book_{index}'
        )
    )
  markup.add(InlineKeyboardButton('⬅️ ወደ ዋናው ማውጫ', callback_data='go_main_menu'))
  return markup


# ----------------------------------------------------
# 5. Command & Text Handlers
# ----------------------------------------------------


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  welcome_text = (
      '📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጽሐፍት» በሰላም መጡ!**\n\n'
      'እባክዎ መጽሐፍትን ለማግኘት የቋንቋ ዘርፍ ይምረጡ፦'
  )
  bot.send_message(
      message.chat.id,
      welcome_text,
      reply_markup=get_language_inline_keyboard(),
      parse_mode='Markdown',
  )
  bot.send_message(
      message.chat.id,
      '👇 ከታች ያሉትን አማራጮች መጠቀም ይችላሉ፦',
      reply_markup=get_main_reply_keyboard(),
  )


@bot.message_handler(
    func=lambda message: message.text
    in ['🏠 Main Menu', '⬅️ Go Back', '/start']
)
def handle_main_menu_button(message):
  send_welcome(message)


@bot.message_handler(
    func=lambda message: message.text == '📚 መንፈሳዊ መጽሐፍት'
)
def handle_books_button(message):
  bot.send_message(
      message.chat.id,
      'እባክዎ መጽሐፍትን ለማግኘት የቋንቋ ዘርፍ ይምረጡ፦',
      reply_markup=get_language_inline_keyboard(),
  )


@bot.message_handler(func=lambda message: message.text == '📞 Contact Me')
def handle_contact(message):
  bot.send_message(
      message.chat.id,
      '📩 **እኛን ለማግኘት፦**\n\nለማንኛውም አስተያየት ወይም ጥያቄ በቴሌግራም ያግኙን።',
      parse_mode='Markdown',
  )


@bot.message_handler(func=lambda message: message.text == '💬 Feedback')
def handle_feedback(message):
  bot.send_message(
      message.chat.id,
      '✍️ **አስተያየትዎን ያስቀምጡ፦**\n\nለቦታችን እድገት የሚረዱ ሃሳቦችን እና አስተያየቶችን ይላኩልን።',
      parse_mode='Markdown',
  )


# ----------------------------------------------------
# 6. Callback Query Handler (የኢንላይን በተኖች ምላሽ)
# ----------------------------------------------------


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  if call.data == 'lang_geez_guide':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='📖 **የግዕዝ መማሪያ መጽሐፍት፦**\n\nለማውረድ የሚፈልጉትን መጽሐፍ ይምረጡ፦',
        reply_markup=get_geez_books_keyboard(),
        parse_mode='Markdown',
    )
  elif call.data.startswith('get_geez_book_'):
    index = int(call.data.split('_')[-1])
    book = GEEZ_BOOKS[index]
    bot.send_message(call.message.chat.id, f"⏳ **{book['title']}** በመላክ ላይ ነው...")
    bot.send_document(call.message.chat.id, book['file_id'])
  elif call.data == 'go_main_menu':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            '📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጽሐፍት» በሰላም መጡ!**\n\n'
            'እባክዎ መጽሐፍትን ለማግኘት የቋንቋ ዘርፍ ይምረጡ፦'
        ),
        reply_markup=get_language_inline_keyboard(),
        parse_mode='Markdown',
    )


# ----------------------------------------------------
# 7. Document Handler (ለአንተ/Admin ብቻ የተገደበ)
# ----------------------------------------------------


@bot.message_handler(content_types=['document'])
def handle_document(message):
  # ከላከው ተጠቃሚ Username ጋር ያጣራል
  sender_username = message.from_user.username
  if sender_username and sender_username.lower() == ADMIN_USERNAME.lower():
    file_id = message.document.file_id
    file_name = message.document.file_name
    bot.reply_to(
        message,
        f'✅ **ፋይሉ ደርሷል!**\n\n**የፋይሉ ስም፦** `{file_name}`\n**File'
        f' ID፦**\n`{file_id}`',
        parse_mode='Markdown',
    )
  else:
    bot.reply_to(
        message,
        'መጽሐፍ ለማስገባት ጥቆማ ካለዎት እባክዎ በ Feedback መስመር ያድርሱን።',
    )


# ----------------------------------------------------
# 8. Start App & Bot
# ----------------------------------------------------
if __name__ == '__main__':
  keep_alive()
  print('Bot is starting...')
  bot.infinity_polling(timeout=10, long_polling_timeout=5)