import logging
import random
import configparser
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from bot.utils import load_questions

# Настроим логирование для отладки
logging.basicConfig(level=logging.INFO)

# Переменные
directions = ['Frontend', 'Backend', 'ML_and_DS', 'Mobile']
levels = ['junior', 'middle', 'senior']

# Сохраняем данные пользователя
user_data = {}

def start(update: Update, context: CallbackContext):
    """Отправляет приветственное сообщение и предлагает выбрать направление."""
    
    text = (
        "👋 Привет! Я помогу тебе подготовиться к техническим собеседованиям.\n\n"
        "Доступные команды:\n"
        "/start — начать тестирование\n"
        "/help — информация о боте\n\n"
        "Выбери направление, чтобы начать 👇"
    )
    
    user_id = update.effective_user.id
    user_data[user_id] = {}

    keyboard = [[d] for d in directions]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text(text, reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext):
    text = (
        "ℹ️ О боте:\n\n"
        "Этот бот поможет вам подготовиться к техническим собеседованиям в следующих направлениях:\n"
        "- Frontend\n"
        "- Backend\n"
        "- Machine Learning и Data Science\n"
        "- Mobile-разработка\n\n"
        "Доступные команды:\n"
        "/start — начать тестирование\n"
        "/help — показать справку\n\n"
        "После выбора направления и уровня сложности вам будет предложено 20 случайных вопросов.\n"
        "В конце теста бот подскажет темы, которые стоит повторить.\n\n"
        "Если возникла ошибка, напишите /start для нового начала."
    )

    update.message.reply_text(text)
    
def choose_direction(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    direction = update.message.text

    if direction not in directions:
        update.message.reply_text('Пожалуйста, выбери направление из списка.')
        return

    user_data[user_id]['direction'] = direction

    keyboard = [[l] for l in levels]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text('Теперь выбери уровень сложности:', reply_markup=reply_markup)

def choose_level(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    level = update.message.text.lower()

    if user_id not in user_data or 'direction' not in user_data[user_id]:
        update.message.reply_text('Пожалуйста, сначала выберите направление через /start.')
        return

    if level not in levels:
        update.message.reply_text('Пожалуйста, выбери уровень сложности из списка.')
        return

    user_data[user_id]['level'] = level

    try:
        questions = load_questions(user_data[user_id]['direction'], level)
    except FileNotFoundError:
        update.message.reply_text('К сожалению, вопросы для этого выбора не найдены.')
        return

    random.shuffle(questions)
    questions = questions[:5]

    user_data[user_id]['questions'] = questions
    user_data[user_id]['current'] = 0
    user_data[user_id]['score'] = 0
    user_data[user_id]['wrong_themes'] = set()

    send_question(update, context)

def send_question(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    questions = user_data[user_id]['questions']
    current = user_data[user_id]['current']

    if current >= len(questions):
        show_results(update, context)
        return

    q = questions[current]
    if 'answers' not in q or not q['answers']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка в вопросе, пропускаем...")
        user_data[user_id]['current'] += 1
        send_question(update, context)
        return

    buttons = []
    for ans in q['answers']:
        buttons.append([InlineKeyboardButton(ans['answer_text'], callback_data=str(ans['answer_id']))])

    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вопрос {current+1}: {q['question']}", reply_markup=reply_markup)

def handle_answer(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    selected_answer_id = int(query.data)
    current = user_data[user_id]['current']
    question = user_data[user_id]['questions'][current]

    if selected_answer_id == question['correct_answer_id']:
        user_data[user_id]['score'] += 1
    else:
        useful_info = question['useful_info']
        if isinstance(useful_info, list):
            useful_info = '\n'.join(useful_info)  # Склеиваем ссылки в строку
        user_data[user_id]['wrong_themes'].add((question['theme'], useful_info))

    user_data[user_id]['current'] += 1
    send_question(update, context)


def show_results(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    score = user_data[user_id]['score']
    total = len(user_data[user_id]['questions'])

    text = f"✅ Тест завершён!\n\nТвой результат: {score}/{total}\n\nТемы для повторения:\n"
    if user_data[user_id]['wrong_themes']:
        for theme, info in user_data[user_id]['wrong_themes']:
            text += f"• {theme}:\n  {info}\n"
    else:
        text += "Отлично! Все темы изучены!"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def main():
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    TOKEN = config['bot']['token']

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(MessageHandler(Filters.regex(f"^({'|'.join(directions)})$"), choose_direction))
    dp.add_handler(MessageHandler(Filters.regex(f"^({'|'.join(levels)})$"), choose_level))
    dp.add_handler(CallbackQueryHandler(handle_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()