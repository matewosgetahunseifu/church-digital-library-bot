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
# የቦትህን Token እዚህ ጋር አረጋግጥ
BOT_TOKEN = os.environ.get(
    'BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE'
)  # ወይም ቀጥታ Tokenህን አስገባ
bot = telebot.TeleBot(BOT_TOKEN)

# ----------------------------------------------------
# 3. Keyboards (የቁልፎች አደረጃጀት)
# ----------------------------------------------------


def get_main_reply_keyboard():
  markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn_books = '📚 መንፈሳዊ መጽሐፍት'
  btn_contact = '📞 Contact Me'
  btn_feedback = '💬 Feedback'
  btn_main_menu = '🏠 Main Menu'

  markup.add(btn_books)
  markup.add(btn_contact, btn_feedback)
  markup.add(btn_main_menu)
  return markup


def get_language_inline_keyboard():
  markup = InlineKeyboardMarkup(row_width=2)
  markup.add(
      InlineKeyboardButton('ግዕዝ', callback_data='lang_geez'),
      InlineKeyboardButton('ግዕዝ-አማርኛ', callback_data='lang_geez_amharic'),
  )
  markup.add(
      InlineKeyboardButton(
          'የግዕዝ ቋንቋ መመሪያ', callback_data='lang_geez_guide'
      )
  )
  markup.add(
      InlineKeyboardButton('አማርኛ', callback_data='lang_amharic'),
      InlineKeyboardButton('English', callback_data='lang_english'),
  )
  return markup


# ----------------------------------------------------
# 4. Command Handlers
# ----------------------------------------------------


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  welcome_text = (
      '📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጽሐፍት» በሰላም መጡ!**\n\n'
      'እባክዎ መጽሐፍትን በምን ቋንቋ ማንበብ ይፈልጋሉ?'
  )
  bot.send_message(
      message.chat.id,
      welcome_text,
      reply_markup=get_language_inline_keyboard(),
      parse_mode='Markdown',
  )

  # ከታች የሚታየውን Main Menu Keyboard ይልካል
  bot.send_message(
      message.chat.id,
      '👇 ከታች ያሉትን አማራጮች መጠቀም ይችላሉ፦',
      reply_markup=get_main_reply_keyboard(),
  )


# ----------------------------------------------------
# 5. Text Message Handlers (Reply Buttons)
# ----------------------------------------------------


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
      'እባክዎ መጽሐፍትን ለማግኘት ቋንቋ ይምረጡ፦',
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
# 6. Document Handler (File ID ለማግኘት)
# ----------------------------------------------------


@bot.message_handler(content_types=['document'])
def handle_document(message):
  file_id = message.document.file_id
  file_name = message.document.file_name
  bot.reply_to(
      message,
      f'✅ **ፋይሉ ደርሷል!**\n\n**የፋይሉ ስም፦** `{file_name}`\n**File'
      f' ID፦**\n`{file_id}`',
      parse_mode='Markdown',
  )


# ----------------------------------------------------
# 7. Start App & Bot
# ----------------------------------------------------
if __name__ == '__main__':
  keep_alive()
  print('Bot is starting...')
  bot.infinity_polling(timeout=10, long_polling_timeout=5)