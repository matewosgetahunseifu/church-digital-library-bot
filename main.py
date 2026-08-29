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

BOT_TOKEN = os.environ.get(
    'BOT_TOKEN', '8777005011:AAHi7FXjLXk9QkRBzylmzsLqYj7dRC1PR_Y'
)
bot = telebot.TeleBot(BOT_TOKEN)

# Admin Username (ለደህንነት የተገደበ)
ADMIN_USERNAME = 'Sealilenemariyammsle12we19'

# 3. Database (የግእዝ መማሪያ መጽሐፍት ዝርዝር)
GEEZ_GUIDE_BOOKS = [
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

# 4. Keyboards Generation Functions


def get_main_reply_keyboard():
  markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  markup.add('📚 መንፈሳዊ መጽሐፍት')
  markup.add('📞 Contact Me', '💬 Feedback')
  markup.add('🏠 Main Menu')
  return markup


# 1. ዋና የቋንቋ መምረጫ ገጽ (Main Menu Inline)
def get_language_inline_keyboard():
  markup = InlineKeyboardMarkup(row_width=2)
  markup.add(
      InlineKeyboardButton('ግእዝ', callback_data='lang_geez'),
      InlineKeyboardButton('ግእዝ-አማርኛ', callback_data='lang_geez_amharic'),
  )
  markup.add(
      InlineKeyboardButton(
          'የግእዝ ቋንቋ መማሪያ', callback_data='lang_geez_guide'
      )
  )
  markup.add(
      InlineKeyboardButton('አማርኛ', callback_data='lang_amharic'),
      InlineKeyboardButton('English', callback_data='lang_english'),
  )
  return markup


# 2. የክፍሎች መምረጫ (Category Selection)
def get_category_keyboard(lang_code):
  markup = InlineKeyboardMarkup(row_width=2)
  if lang_code == 'english':
    markup.add(
        InlineKeyboardButton(
            'Law & Order', callback_data=f'cat_{lang_code}_law'
        ),
        InlineKeyboardButton(
            'History & Discourse', callback_data=f'cat_{lang_code}_history_main'
        ),
    )
    markup.add(
        InlineKeyboardButton(
            'Theology', callback_data=f'cat_{lang_code}_theology'
        ),
        InlineKeyboardButton(
            'Christian Ethics', callback_data=f'cat_{lang_code}_ethics'
        ),
    )
    markup.add(
        InlineKeyboardButton(
            'Holy Bible Section', callback_data=f'cat_{lang_code}_bible'
        )
    )
    markup.add(InlineKeyboardButton('🔙 Go Back', callback_data='go_main_menu'))
  else:
    markup.add(
        InlineKeyboardButton(
            'ሕግና ሥርዓት', callback_data=f'cat_{lang_code}_law'
        ),
        InlineKeyboardButton(
            'ታሪክና ድርሳናት', callback_data=f'cat_{lang_code}_history_main'
        ),
    )
    markup.add(
        InlineKeyboardButton(
            'ነገረ ሃይማኖት', callback_data=f'cat_{lang_code}_theology'
        ),
        InlineKeyboardButton(
            'ክርስቲያናዊ ሥነ ምግባር', callback_data=f'cat_{lang_code}_ethics'
        ),
    )
    markup.add(
        InlineKeyboardButton(
            'የመጽሐፍ ቅዱስ ክፍል', callback_data=f'cat_{lang_code}_bible'
        )
    )
    markup.add(
        InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='go_main_menu')
    )
  return markup


# 3. የታሪክና ድርሳናት ንኡስ ክፍል መምረጫ (Sub-category for History)
def get_history_subcategory_keyboard(lang_code):
  markup = InlineKeyboardMarkup(row_width=1)
  if lang_code == 'english':
    markup.add(
        InlineKeyboardButton(
            '1. History', callback_data=f'sub_{lang_code}_history'
        )
    )
    markup.add(
        InlineKeyboardButton(
            '2. Discourse, Hagiography & Miracles',
            callback_data=f'sub_{lang_code}_hagiography',
        )
    )
    markup.add(
        InlineKeyboardButton(
            '🔙 Go Back', callback_data=f'back_to_lang_{lang_code}'
        )
    )
  else:
    markup.add(
        InlineKeyboardButton(
            '1. ታሪክ', callback_data=f'sub_{lang_code}_history'
        )
    )
    markup.add(
        InlineKeyboardButton(
            '2. ድርሳን፣ ገድልና ተአምር', callback_data=f'sub_{lang_code}_hagiography'
        )
    )
    markup.add(
        InlineKeyboardButton(
            '🔙 ወደ ኋላ ይመለሱ', callback_data=f'back_to_lang_{lang_code}'
        )
    )
  return markup


# 4. የግእዝ መማሪያ መጽሐፍት ዝርዝር
def get_geez_guide_books_keyboard():
  markup = InlineKeyboardMarkup(row_width=1)
  for index, book in enumerate(GEEZ_GUIDE_BOOKS):
    markup.add(
        InlineKeyboardButton(
            book['title'], callback_data=f'get_geez_book_{index}'
        )
    )
  markup.add(
      InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='go_main_menu')
  )
  return markup

# 5. Handlers & Bot Logic



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  welcome_text = (
      '📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጻሕፍት» በደኅና መጡ!**\n\n'
      'እባክዎ መጽሐፍትን በምን ቋንቋ ማንበብ ይፈልጋሉ?'
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
      'እባክዎ መጽሐፍትን በምን ቋንቋ ማንበብ ይፈልጋሉ?',
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

# 6. Callback Queries (Inline Keyboard Event Handling)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  data = call.data

  # 1. ወደ ዋና ማውጫ የመመለሻ በተን
  if data == 'go_main_menu':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            '📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጻሕፍት» በደኅና መጡ!**\n\n'
            'እባክዎ መጽሐፍትን በምን ቋንቋ ማንበብ ይፈልጋሉ?'
        ),
        reply_markup=get_language_inline_keyboard(),
        parse_mode='Markdown',
    )

  # 2. የቋንቋ ምርጫዎች
  elif data == 'lang_geez':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='📖 የተመረጠው ቋንቋ፦ 📜 **ግዕዝ**\n\nእባክዎ በግእዝ ምን ማንበብ ይፈልጋሉ?',
        reply_markup=get_category_keyboard('geez'),
        parse_mode='Markdown',
    )

  elif data == 'lang_geez_amharic':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            '📖 የተመረጠው ቋንቋ፦ 🇪🇹 **ግዕዝ አማርኛ**\n\n'
            'እባክዎ በግእዝ አማርኛ ምን ማንበብ ይፈልጋሉ?'
        ),
        reply_markup=get_category_keyboard('geez_amharic'),
        parse_mode='Markdown',
    )

  elif data == 'lang_geez_guide':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='📖 **የግእዝ ቋንቋ መመሪያ (መማሪያ መጽሐፍት)፦**\n\nእባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦',
        reply_markup=get_geez_guide_books_keyboard(),
        parse_mode='Markdown',
    )

  elif data == 'lang_amharic':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='📖 የተመረጠው ቋንቋ፦ **አማርኛ**\n\nእባክዎ በአማርኛ ምን ማንበብ ይፈልጋሉ?',
        reply_markup=get_category_keyboard('amharic'),
        parse_mode='Markdown',
    )

  elif data == 'lang_english':
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            '📖 Selected Language: 🇬🇧 **English**\n\nPlease choose what you would'
            ' like to read in English:'
        ),
        reply_markup=get_category_keyboard('english'),
        parse_mode='Markdown',
    )

  # 3. ወደ ቋንቋ መምረጫ መመለሻ 
  elif data.startswith('back_to_lang_'):
    lang_code = data.replace('back_to_lang_', '')
    if lang_code == 'english':
      bot.edit_message_text(
          chat_id=call.message.chat.id,
          message_id=call.message.message_id,
          text=(
              '📖 Selected Language: 🇬🇧 **English**\n\nPlease choose what you'
              ' would like to read in English:'
          ),
          reply_markup=get_category_keyboard('english'),
          parse_mode='Markdown',
      )
    else:
      bot.edit_message_text(
          chat_id=call.message.chat.id,
          message_id=call.message.message_id,
          text='እባክዎ ምን ማንበብ ይፈልጋሉ?',
          reply_markup=get_category_keyboard(lang_code),
          parse_mode='Markdown',
      )

  # 4. ታሪክና ድርሳናት ሲነካ
  elif data.endswith('_history_main'):
    lang_code = data.split('_')[1]
    msg = (
        'Please select one of the following options:'
        if lang_code == 'english'
        else 'እባክዎ ከታች ካሉት አማራጮች አንዱን ይምረጡ፦'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=msg,
        reply_markup=get_history_subcategory_keyboard(lang_code),
        parse_mode='Markdown',
    )

  # 5. መጽሐፍት ማውረጃና ዝርዝር
  elif data.startswith('get_geez_book_'):
    index = int(data.split('_')[-1])
    book = GEEZ_GUIDE_BOOKS[index]
    bot.send_message(
        call.message.chat.id, f"ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n\"{book['title']}\"\n\nመልካም ንባብ ይሁንሎት! 📖✨"
    )
    bot.send_document(call.message.chat.id, book['file_id'])

  # ለሌሎቹ ባዶ ክፍሎች የሚሰጥ ጊዜያዊ ምላሽ
  elif data.startswith('cat_') or data.startswith('sub_'):
    is_eng = 'english' in data
    text_msg = (
        'Please select the book you would like to read:\n\n*(No books added to'
        ' this section yet)*'
        if is_eng
        else 'እባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦\n\n*(በዚህ ክፍል እስካሁን የገቡ መጽሐፍት የሉም)*'
    )
    back_btn_text = '🔙 Go Back' if is_eng else '🔙 ወደ ኋላ ይመለሱ'

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('🔙 ወደ ኋላ ይመለሱ', callback_data='go_main_menu')
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text_msg,
        reply_markup=markup,
        parse_mode='Markdown',
    )

# 7. Document Handler (ለAdmin ብቻ የተገደበ)


@bot.message_handler(content_types=['document'])
def handle_document(message):
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

# 8. App Launch

if __name__ == '__main__':
  keep_alive()
  print('Bot is starting...')
  bot.infinity_polling(timeout=10, long_polling_timeout=5)
  #comment