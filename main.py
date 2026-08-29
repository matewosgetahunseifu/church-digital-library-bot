import os
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# --- Web Server setup for Render Keep-Alive ---
app = Flask(__name__)


@app.route('/')
def home():
  return 'Bot is running alive!'


def run():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()


# 1. ቦት ቶከን
TOKEN = '8777005011:AAHi7FXjLXk9QkRBzylmzsLqYj7dRC1PR_Y'

bot = telebot.TeleBot(TOKEN)

# 2. የመጽሐፍት Database
BOOKS_DB = {
    'lang_geez': {
        'title': '📜 ግዕዝ',
        'subcats': {
            'law': {
                'title': 'ሕግና ሥርዓት',
                'books': [
                    {'title': 'ፍትሐ ነገሥት (ግዕዝ)', 'file_id': ''},
                    {
                        'title': 'መጽሐፈ ሐዊ',
                        'file_id': (
                            'BQACAgQAAxkBAAMYapE9Ut5EsV4vgke4j61_9Zx2uAsAAmcKAAKIvhFR0bgLZxeycwg9BA'
                        ),
                    },
                ],
            },
            'history_group': {
                'title': 'ታሪክና ድርሳናት',
                'types': {
                    'history': {
                        'title': '1. ታሪክ',
                        'books': [
                            {
                                'title': 'ታሪከ ኢትዮጵያ በልሳነ ግእዝ',
                                'file_id': (
                                    'BQACAgQAAxkBAAMwapFf7bV4pZlUFsg17AAB2INtea0IAALlFwACEa5YU0RdEqkyYFWQPQQ'
                                ),
                            },
                            {
                                'title': 'ዜና እስክንድር',
                                'file_id': (
                                    'BQACAgQAAxkBAAMxapFf7XOrycl8ofSEBFVR4HiGMc8AAiYRAAI1tJFT9VnEitLhIJ89BA'
                                ),
                            },
                            {
                                'title': 'መጽሐፈ አክሱም',
                                'file_id': (
                                    'BQACAgQAAxkBAAMyapFf7YV3aZpveR4LrqxQmc83P84AAjQZAALDX3FTvkQc4RygGTA9BA'
                                ),
                            },
                        ],
                    },
                    'dersan': {
                        'title': '2. ድርሳን፣ ገድልና ተአምር',
                        'books': [{
                            'title': 'መጽሐፈ ልደታ ለማርያም',
                            'file_id': (
                                'BQACAgQAAxkBAAMzapFf7X3q2oIBy2xFDKAsrQlayGwAAv0XAALDX3FTAAH2eGNJvid8PQQ'
                            ),
                        }],
                    },
                },
            },
            'theology': {'title': 'ነገረ ሃይማኖት', 'books': []},
            'ethics': {'title': 'ክርስቲያናዊ ሥነ ምግባር', 'books': []},
            'bible': {'title': 'የመጽሐፍ ቅዱስ ክፍል', 'books': []},
        },
    },
    'lang_geez_amharic': {
        'title': '🇪🇹 ግዕዝ አማርኛ',
        'subcats': {
            'law': {'title': 'ሕግና ሥርዓት', 'books': []},
            'history_group': {
                'title': 'ታሪክና ድርሳናት',
                'types': {
                    'history': {'title': '1. ታሪክ', 'books': []},
                    'dersan': {
                        'title': '2. ድርሳን፣ ገድልና ተአምር',
                        'books': [{
                            'title': 'መጽሐፈ ገነት ዘውእቱ ዜና አበው',
                            'file_id': (
                                'BQACAgQAAxkBAAMsapFfp6Q7I10ZZzZGN9P8VBJ4b1kAAjUHAAIWouhQcHtGpw5LDv49BA'
                            ),
                        }],
                    },
                },
            },
            'theology': {'title': 'ነገረ ሃይማኖት', 'books': []},
            'ethics': {'title': 'ክርስቲያናዊ ሥነ ምግባር', 'books': []},
            'bible': {'title': 'የመጽሐፍ ቅዱስ ክፍል', 'books': []},
        },
    },
    'lang_geez_learning': {
        'title': '📖 የግዕዝ ቋንቋ መማሪያ',
        'books': [{'title': 'መጽሐፈ ሰዋስው ወግሥ (የግእዝ መማሪያ)', 'file_id': ''}],
    },
    'lang_amharic': {
        'title': 'አማርኛ',
        'subcats': {
            'law': {'title': 'ሕግና ሥርዓት', 'books': []},
            'history_group': {
                'title': 'ታሪክና ድርሳናት',
                'types': {
                    'history': {'title': '1. ታሪክ', 'books': []},
                    'dersan': {'title': '2. ድርሳን፣ ገድልና ተአምር', 'books': []},
                },
            },
            'theology': {'title': 'ነገረ ሃይማኖት', 'books': []},
            'ethics': {'title': 'ክርስቲያናዊ ሥነ ምግባር', 'books': []},
            'bible': {'title': 'የመጽሐፍ ቅዱስ ክፍል', 'books': []},
        },
    },
    'lang_english': {
        'title': '🇬🇧 English',
        'subcats': {
            'law': {'title': 'Law & Order', 'books': []},
            'history_group': {
                'title': 'History & Discourse',
                'types': {
                    'history': {'title': '1. History', 'books': []},
                    'dersan': {
                        'title': '2. Discourse, Hagiography & Miracles',
                        'books': [],
                    },
                },
            },
            'theology': {'title': 'Theology', 'books': []},
            'ethics': {'title': 'Christian Ethics', 'books': []},
            'bible': {'title': 'Holy Bible Section', 'books': []},
        },
    },
}


# 3. Start Command Handler
@bot.message_handler(commands=['start'])
def start_cmd(message):
  reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
  reply_markup.row(KeyboardButton('📚 መንፈሳዊ መጽሐፍት'))
  reply_markup.row(
      KeyboardButton('📞 Contact Me'), KeyboardButton('💬 Feedback')
  )
  reply_markup.row(KeyboardButton('⬅️ Go Back'))

  inline_markup = InlineKeyboardMarkup()
  inline_markup.row(
      InlineKeyboardButton(text='ግእዝ', callback_data='lang:lang_geez'),
      InlineKeyboardButton(
          text='ግእዝ-አማርኛ', callback_data='lang:lang_geez_amharic'
      ),
  )
  inline_markup.row(
      InlineKeyboardButton(
          text='የግዕዝ ቋንቋ መማሪያ', callback_data='lang:lang_geez_learning'
      )
  )
  inline_markup.row(
      InlineKeyboardButton(text='አማርኛ', callback_data='lang:lang_amharic'),
      InlineKeyboardButton(text='English', callback_data='lang:lang_english'),
  )

  bot.send_message(
      message.chat.id,
      '📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጻሕፍት» በደኅና መጡ!**\n\nእባክዎ መጽሐፍትን'
      ' በምን ቋንቋ ማንበብ ይፈልጋሉ?',
      parse_mode='Markdown',
      reply_markup=inline_markup,
  )
  bot.send_message(message.chat.id, '👇', reply_markup=reply_markup)


# 4. Reply Keyboard Handler
@bot.message_handler(
    func=lambda message: message.text
    in ['📚 መንፈሳዊ መጽሐፍት', '💬 Feedback', '📞 Contact Me', '⬅️ Go Back']
)
def handle_reply_buttons(message):
  if message.text in ['📚 መንፈሳዊ መጽሐፍት', '⬅️ Go Back']:
    start_cmd(message)
  elif message.text == '💬 Feedback':
    bot.reply_to(
        message,
        '💬 **አስተያየትዎን ያድርሱን፦**\n\nለማንኛውም ጥያቄ፣ አስተያየት ወይም ተጨማሪ መጽሐፍ'
        ' ጥቆማ በቴሌግራም አድራሻችን ያግኙን፦\n👉 @Sealilenemariyammsle12we19',
        parse_mode='Markdown',
    )
  elif message.text == '📞 Contact Me':
    bot.reply_to(
        message,
        '📞 **ለተጨማሪ መረጃ እና ግንኙነት፦**\n\n• **Telegram:**'
        ' @Sealilenemariyammsle12we19\n• **Email:**'
        ' matewosgetahunseifu@gmail.com',
        parse_mode='Markdown',
    )


# 5. Inline Callback Query Handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  data = call.data.split(':')
  chat_id = call.message.chat.id
  message_id = call.message.message_id

  # 1. የቋንቋ መምረጫ
  if data[0] == 'lang':
    lang_key = data[1]
    lang_data = BOOKS_DB[lang_key]
    markup = InlineKeyboardMarkup()

    if lang_key == 'lang_geez_learning':
      for idx, book in enumerate(lang_data.get('books', [])):
        markup.row(
            InlineKeyboardButton(
                text=book['title'],
                callback_data=f'directbook:{lang_key}:{idx}',
            )
        )
      markup.row(
          InlineKeyboardButton(
              text='🔙 ወደ ኋላ ይመለሱ', callback_data='main_menu'
          )
      )

      msg_text = 'እባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦'
      bot.edit_message_text(
          msg_text,
          chat_id,
          message_id,
          parse_mode='Markdown',
          reply_markup=markup,
      )

    else:
      subcats = lang_data['subcats']
      markup.row(
          InlineKeyboardButton(
              text=subcats['law']['title'],
              callback_data=f'sub:{lang_key}:law',
          ),
          InlineKeyboardButton(
              text=subcats['history_group']['title'],
              callback_data=f'sub:{lang_key}:history_group',
          ),
      )
      markup.row(
          InlineKeyboardButton(
              text=subcats['theology']['title'],
              callback_data=f'sub:{lang_key}:theology',
          ),
          InlineKeyboardButton(
              text=subcats['ethics']['title'],
              callback_data=f'sub:{lang_key}:ethics',
          ),
      )
      markup.row(
          InlineKeyboardButton(
              text=subcats['bible']['title'],
              callback_data=f'sub:{lang_key}:bible',
          )
      )

      back_btn_text = (
          '🔙 Go Back' if lang_key == 'lang_english' else '🔙 ወደ ኋላ ይመለሱ'
      )
      markup.row(
          InlineKeyboardButton(text=back_btn_text, callback_data='main_menu')
      )

      if lang_key == 'lang_english':
        msg_text = (
            f"📖 **Selected Language: {lang_data['title']}**\n\nPlease choose"
            ' what you would like to read in English:'
        )
      else:
        msg_text = (
            f"📖 **የተመረጠው ቋንቋ፦ {lang_data['title']}**\n\nእባክዎ"
            f" በ{lang_data['title']} ምን ማንበብ ይፈልጋሉ?"
        )

      bot.edit_message_text(
          msg_text,
          chat_id,
          message_id,
          parse_mode='Markdown',
          reply_markup=markup,
      )

  # 2. የካቴጎሪ መምረጫ
  elif data[0] == 'sub':
    lang_key, sub_key = data[1], data[2]
    subcat = BOOKS_DB[lang_key]['subcats'][sub_key]
    markup = InlineKeyboardMarkup()
    back_btn_text = (
        '🔙 Go Back' if lang_key == 'lang_english' else '🔙 ወደ ኋላ ይመለሱ'
    )

    if 'types' in subcat:
      for type_key, type_data in subcat['types'].items():
        markup.row(
            InlineKeyboardButton(
                text=type_data['title'],
                callback_data=f'type:{lang_key}:{sub_key}:{type_key}',
            )
        )
      markup.row(
          InlineKeyboardButton(
              text=back_btn_text, callback_data=f'lang:{lang_key}'
          )
      )

      msg_text = (
          'Please select one of the following options:'
          if lang_key == 'lang_english'
          else 'እባክዎ ከታች ከተዘረዘሩት ንኡስ ክፍሎች ይምረጡ፦'
      )
      bot.edit_message_text(
          msg_text,
          chat_id,
          message_id,
          parse_mode='Markdown',
          reply_markup=markup,
      )

    elif 'books' in subcat:
      for idx, book in enumerate(subcat['books']):
        markup.row(
            InlineKeyboardButton(
                text=book['title'],
                callback_data=f'book:{lang_key}:{sub_key}:{idx}',
            )
        )
      markup.row(
          InlineKeyboardButton(
              text=back_btn_text, callback_data=f'lang:{lang_key}'
          )
      )

      msg_text = (
          'Please select the book you would like to read:'
          if lang_key == 'lang_english'
          else 'እባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦'
      )
      bot.edit_message_text(
          msg_text,
          chat_id,
          message_id,
          parse_mode='Markdown',
          reply_markup=markup,
      )

  # 3. ንኡስ ክፍሎች የመጽሐፍ ዝርዝር
  elif data[0] == 'type':
    lang_key, sub_key, type_key = data[1], data[2], data[3]
    type_data = BOOKS_DB[lang_key]['subcats'][sub_key]['types'][type_key]
    markup = InlineKeyboardMarkup()
    back_btn_text = (
        '🔙 Go Back' if lang_key == 'lang_english' else '🔙 ወደ ኋላ ይመለሱ'
    )

    for idx, book in enumerate(type_data.get('books', [])):
      markup.row(
          InlineKeyboardButton(
              text=book['title'],
              callback_data=f'booktype:{lang_key}:{sub_key}:{type_key}:{idx}',
          )
      )

    markup.row(
        InlineKeyboardButton(
            text=back_btn_text, callback_data=f'sub:{lang_key}:{sub_key}'
        )
    )

    msg_text = (
        'Please select the book you would like to read:'
        if lang_key == 'lang_english'
        else 'እባክዎ ማንበብ የሚፈልጉትን መጽሐፍ ይምረጡ፦'
    )
    bot.edit_message_text(
        msg_text, chat_id, message_id, parse_mode='Markdown', reply_markup=markup
    )

  # 4. መጽሐፍ ሲላክ (ቀጥታ ካቴጎሪዎች)
  elif data[0] == 'book':
    lang_key, sub_key, book_idx = data[1], data[2], int(data[3])
    book = BOOKS_DB[lang_key]['subcats'][sub_key]['books'][book_idx]
    markup = InlineKeyboardMarkup()
    back_btn_text = (
        '🔙 Go Back' if lang_key == 'lang_english' else '🔙 ወደ ኋላ ይመለሱ'
    )
    markup.row(
        InlineKeyboardButton(
            text=back_btn_text, callback_data=f'sub:{lang_key}:{sub_key}'
        )
    )

    if book.get('file_id'):
      caption = (
          f'ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n"{book["title"]}"\nመልካም ንባብ ይሁንሎት! 📖✨'
          if lang_key != 'lang_english'
          else f'Here is the book you requested to read:\n"{book["title"]}"\nHave'
          ' a wonderful reading time! 📖✨'
      )
      bot.send_document(
          chat_id, book['file_id'], caption=caption, reply_markup=markup
      )
    else:
      bot.send_message(
          chat_id,
          f"⚠️ **{book['title']}** መጽሐፍ በአሁኑ ወቅት አልተካተተበትም።",
          reply_markup=markup,
      )

  # 5. መጽሐፍ ሲላክ (ከታሪክና ድርሳናት ንኡስ ክፍሎች)
  elif data[0] == 'booktype':
    lang_key, sub_key, type_key, book_idx = (
        data[1],
        data[2],
        data[3],
        int(data[4]),
    )
    book = BOOKS_DB[lang_key]['subcats'][sub_key]['types'][type_key]['books'][
        book_idx
    ]
    markup = InlineKeyboardMarkup()
    back_btn_text = (
        '🔙 Go Back' if lang_key == 'lang_english' else '🔙 ወደ ኋላ ይመለሱ'
    )
    markup.row(
        InlineKeyboardButton(
            text=back_btn_text,
            callback_data=f'type:{lang_key}:{sub_key}:{type_key}',
        )
    )

    if book.get('file_id'):
      caption = (
          f'ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n"{book["title"]}"\nመልካም ንባብ ይሁንሎት! 📖✨'
          if lang_key != 'lang_english'
          else f'Here is the book you requested to read:\n"{book["title"]}"\nHave'
          ' a wonderful reading time! 📖✨'
      )
      bot.send_document(
          chat_id, book['file_id'], caption=caption, reply_markup=markup
      )
    else:
      bot.send_message(
          chat_id,
          f"⚠️ **{book['title']}** መጽሐፍ በአሁኑ ወቅት አልተካተተበትም።",
          reply_markup=markup,
      )

  # 6. መጽሐፍ ሲላክ (ቀጥታ ከቋንቋ መማሪያ ስር)
  elif data[0] == 'directbook':
    lang_key, book_idx = data[1], int(data[2])
    book = BOOKS_DB[lang_key]['books'][book_idx]
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='🔙 ወደ ኋላ ይመለሱ', callback_data=f'lang:{lang_key}'
        )
    )

    if book.get('file_id'):
      caption = (
          f'ለማንበብ የፈለጉት መጽሐፍ ይኸው፦\n"{book["title"]}"\nመልካም ንባብ ይሁንሎት! 📖✨'
      )
      bot.send_document(
          chat_id, book['file_id'], caption=caption, reply_markup=markup
      )
    else:
      bot.send_message(
          chat_id,
          f"⚠️ **{book['title']}** መጽሐፍ በአሁኑ ወቅት አልተካተተበትም።",
          reply_markup=markup,
      )

  # 7. ወደ ዋናው ገጽ መመለሻ
  elif data[0] == 'main_menu':
    inline_markup = InlineKeyboardMarkup()
    inline_markup.row(
        InlineKeyboardButton(text='ግእዝ', callback_data='lang:lang_geez'),
        InlineKeyboardButton(
            text='ግእዝ-አማርኛ', callback_data='lang:lang_geez_amharic'
        ),
    )
    inline_markup.row(
        InlineKeyboardButton(
            text='የግዕዝ ቋንቋ መማሪያ', callback_data='lang:lang_geez_learning'
        )
    )
    inline_markup.row(
        InlineKeyboardButton(text='አማርኛ', callback_data='lang:lang_amharic'),
        InlineKeyboardButton(text='English', callback_data='lang:lang_english'),
    )

    bot.edit_message_text(
        '📚 **እንኳን ወደ «መንፈሳዊ ዲጂታል ቤተ-መጻሕፍት» በደኅና መጡ!**\n\nእባክዎ መጽሐፍትን'
        ' በምን ቋንቋ ማንበብ ይፈልጋሉ?',
        chat_id,
        message_id,
        parse_mode='Markdown',
        reply_markup=inline_markup,
    )


# 6. Document Handler
@bot.message_handler(content_types=['document'])
def handle_document(message):
  file_id = message.document.file_id
  file_name = message.document.file_name
  bot.reply_to(
      message,
      f'✅ **ፋይሉ ደርሷል!**\n\n**የፋይሉ ስም፦** `{file_name}`\n**File'
      f' ID፦**\n`{file_id}`\n\nይህንን `file_id` ኮፒ በማድረግ በኮድዎ `BOOKS_DB` ውስጥ'
      ' ማስገባት ይችላሉ።',
      parse_mode='Markdown',
  )


# --- Web Server አስጀምር ከዚያ ቦቱን አስጀምር ---
keep_alive()

print('ቦቱ በስኬት ሥራ ጀምሯል...')

# 7. Polling Execution
bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=10)