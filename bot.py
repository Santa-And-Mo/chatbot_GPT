from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, filters

from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu, load_prompt, send_text_buttons, Dialog)

import credentials

# обробка кнопок на сторінці "Випадковий факт"
async def default_callback_handler(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if query == "more_btn":            # Кнопка "Хочу ще факт"
        await random(update, context)
    elif query == "end_btn":            # Кнопка "Закінчити"
        await start(update, context)   # Перехід в меню Start"


# Головне меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "default"
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Головне меню',
        'random': 'Дізнатися випадковий цікавий факт 🧠',
        'gpt': 'Задати питання чату GPT 🤖',
        'talk': 'Поговорити з відомою особистістю 👤',
        'quiz': 'Взяти участь у квізі ❓'
        # Додати команду в меню можна так:
        # 'command': 'button text'

    })

# цікавий факт від GPT
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "random"
    text = load_message("random")
    await send_image(update, context, "random")
    await send_text(update, context, text)
    prompt = load_prompt("random")
    content = await chat_gpt.send_question(prompt, "Дай цікавий факт")
    await send_text_buttons(update, context, content, {
        "more_btn": "Хочу ще факт",
        "end_btn": "Закінчити"
    })
# питання до GPT
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_image(update, context, "gpt")
    await send_text(update, context, text)

# отримуємо відповідь від GPT
async def handle_gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gpt_message = update.message.text
    return gpt_message
    # print(gpt_message)

# отримуємо запитання від користувача та відображаємо в терміналі
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    print(f"Користувач запитав: {question}") # перевірка тексту запитання
    if dialog.mode == "gpt":
        await handle_gpt_message(update, context)

# перевіряємо текст запитання на довжину
    if len(question) > 500:
        await send_text(update, context, "Your question is too long.")
        return
# завантажуємо промпт для GPT
    prompt = load_prompt("gpt")
# відправляємо промпт та питання до GPT
    content = await chat_gpt.send_question(prompt, question)

# Надсилання відповіді від GPT користувачу
    await send_text(update, context, content)
# отримуємо відповідь від GPT та направляємо в термінал
    answer = await chat_gpt.send_message_list()
    print(answer)

dialog = Dialog()
dialog.mode = "default"

chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
app = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

# Зареєструвати обробник команди можна так:
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))

app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(MessageHandler(filters.TEXT, handle_message))


# Зареєструвати обробник колбеку можна так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
