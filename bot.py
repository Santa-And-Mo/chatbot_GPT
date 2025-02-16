from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, filters, \
    ConversationHandler
from gpt import ChatGptService
from util import (load_message, send_html, send_text, send_image, show_main_menu, load_prompt, send_text_buttons, Dialog)

import credentials

# обробка кнопок
async def default_callback_handler(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if dialog.mode == "random":
        if query == "more_btn":            # Кнопка "Хочу ще факт"
            await random(update, context)
        elif query == "end_btn":            # Кнопка "Закінчити"
            await start(update, context)   # Перехід в меню Start"
    elif dialog.mode == "talk":
        if query == "cobain_talk_btn":
            dialog.mode = "cobain_talk"
            await talk_cobain(update, context)
        elif query == "hawking_talk_btn":
            dialog.mode = "hawking_talk"
            await talk_hawking(update, context)
        elif query == "nietzsche_talk_btn":
            await talk_nietzsche(update, context)
        elif query == "queen_talk_btn":
            await talk_queen(update, context)
        elif query == "tolkien_talk_btn":
            await talk_tolkien(update, context)
    elif query == "end_talk_btn":            # Кнопка "Закінчити"
        await talk(update, context)          # Перехід в меню Start"
    elif dialog.mode == "quiz":
        if query == "quiz_prog":
            dialog.mode = "quiz_prog"
            await quiz_prog(update, context)
    elif query == "end_btn":                 # Кнопка "Закінчити"
        await start(update, context)         # Перехід в меню Start"


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

### 1. цікавий факт від GPT
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "random"
    text = load_message("random")
    await send_image(update, context, "random")
    await send_text(update, context, text)
    prompt = load_prompt("random")
    content = await chat_gpt.send_question(prompt, "Дай цікавий факт")
    await send_text_buttons(update, context, content,{
        "more_btn": "Хочу ще факт",
        "end_btn": "Закінчити"
    })

### 2. *"ChatGPT інтерфейс"*
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_image(update, context, "gpt")
    await send_text(update, context, text)

# отримуємо запитання від користувача та ведемо діалоги
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    correct_answers_count = 0
    if update.message and update.message.text:
        question = update.message.text
    else:
        question = "  "
    print("Отримано оновлення без повідомлення")
    print(f"Користувач запитав що: {question}") # перевірка тексту запитання в терміналі
    if len(question) > 500:   # перевіряємо текст запитання на довжину
        await send_text(update, context, "Your question is too long, no more 500 characters.")
        return

    if dialog.mode == "gpt":
        prompt = load_prompt("gpt")  # завантажуємо промпт для GPT
        content = await chat_gpt.send_question(prompt, question)  # відправляємо промпт та питання до GPT
        await send_text(update, context, content)  # Надсилання відповіді від GPT користувачу
        answer = await chat_gpt.send_message_list()  # отримуємо відповідь від GPT та направляємо в термінал
        print(answer)

    elif dialog.mode == "cobain_talk":
        prompt = load_prompt("talk_cobain")
        # print(prompt)
        content = await chat_gpt.send_question(prompt, question)
        await send_text(update, context, content)
        print(content)

        content = "Якщо хочете перейти до головного меню"
        await send_text_buttons(update, context, content, {
                 "end_talk_btn": "Вибрати іншу відому особу",
                 "end_btn": "Закінчити"
        })
    elif dialog.mode == "hawking_talk":
        prompt = load_prompt("talk_hawking")
        # print(prompt)
        content = await chat_gpt.send_question(prompt, question)
        await send_text(update, context, content)
        print(content)

        content = "Якщо хочете перейти до головного меню"
        await send_text_buttons(update, context, content, {
                 "end_talk_btn": "Вибрати іншу відому особу",
                 "end_btn": "Закінчити"
        })
    elif dialog.mode == "nietzsche_talk":
        prompt = load_prompt("talk_nietzsche")
        # print(prompt)
        content = await chat_gpt.send_question(prompt, question)
        await send_text(update, context, content)
        print(content)

        content = "Якщо хочете перейти до головного меню"
        await send_text_buttons(update, context, content, {
                 "end_talk_btn": "Вибрати іншу відому особу",
                 "end_btn": "Закінчити"
        })

    elif dialog.mode == "queen_talk":
        prompt = load_prompt("talk_queen")
        # print(prompt)
        content = await chat_gpt.send_question(prompt, question)
        await send_text(update, context, content)
        print(content)

        content = "Якщо хочете перейти до головного меню"
        await send_text_buttons(update, context, content, {
                 "end_talk_btn": "Вибрати іншу відому особу",
                 "end_btn": "Закінчити"
        })

    elif dialog.mode == "tolkien_talk":
        prompt = load_prompt("talk_tolkien")
        # print(prompt)
        content = await chat_gpt.send_question(prompt, question)
        await send_text(update, context, content)
        print(content)

        content = "Якщо хочете перейти до головного меню"
        await send_text_buttons(update, context, content, {
                 "end_talk_btn": "Вибрати іншу відому особу",
                 "end_btn": "Закінчити"
        })

    elif dialog.mode == "quiz_prog":
        prompt = load_prompt("quiz")
        answer = await chat_gpt.send_question(prompt, question)
        await send_text(update, context, answer)
        print(f" GPT answer: {answer}")

        if answer.strip().lower() == "правильно!":
            correct_answers_count += 1
            await send_text(update, context, f"Відповідь правильна! ✅ Загальна кількість: {correct_answers_count}")
        elif answer.strip().lower() == "неправильно!":
            await send_text(update, context, f"Неправильно. ❌ Правильних відповідей: {correct_answers_count}")

        content = "Щоб продовжити напиши: quiz prog"
        await send_text_buttons(update, context, content, {
                 # "quiz_more": "питання на ту ж тему",
                 "end_btn": "Головне меню"
        })

### 3. "Діалог з відомою особистістю"
async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "talk"
    text = load_message("talk")
    await send_image(update, context, "talk")
    await send_text(update, context, text)
    content = "Вибери відому особистість"
    await send_text_buttons(update, context, content, {
        "cobain_talk_btn": "Курт Кобейн - Соліст гурту Nirvana",
        "hawking_talk_btn": "Стівен Гокінг - Фізик",
        "nietzsche_talk_btn": "Фрідріх Ніцше - Філософ",
        "queen_talk_btn": "Єлизавета II - Королева Об'єднаного Королівства",
        "tolkien_talk_btn": "Джон Толкін - Автор книги Володар Перснів",
        "end_btn": "Закінчити"
    })

## Курт Кобейн, легендарний фронтмен гурту Nirvana.
async def talk_cobain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "cobain_talk"
    text = "Мене звати Курт Кобейн. Я Соліст гурту Nirvana."
    await send_image(update, context, "talk_cobain")
    await send_text(update, context, text)
    await handle_message(update, context)

## Стівен Гокінг - Фізик
async def talk_hawking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "hawking_talk"
    text = "Мене звати Стівен Гокінг. Я Фізик"
    await send_image(update, context, "talk_hawking")
    await send_text(update, context, text)
    await handle_message(update, context)

## Фрідріх Ніцше - Філософ
async def talk_nietzsche(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "nietzsche_talk"
    text = "Мене звати Фрідріх Ніцше - Філософ"
    await send_image(update, context, "talk_nietzsche")
    await send_text(update, context, text)
    await handle_message(update, context)

## Єлизавета II - Королева Об'єднаного Королівства
async def talk_queen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "queen_talk"
    text = "Я - Єлизавета II - Королева Об'єднаного Королівства"
    await send_image(update, context, "talk_queen")
    await send_text(update, context, text)
    await handle_message(update, context)

## Джон Толкін - Автор книги "Володар Перснів"
async def talk_tolkien(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "tolkien_talk"
    text = "Моє ім'я - Джон Толкін. Я - Автор книги ""Володар Перснів"""
    await send_image(update, context, "talk_tolkien")
    await send_text(update, context, text)
    await handle_message(update, context)

### 4. *"Квіз"*
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "quiz"
    text = load_message("quiz")
    await send_image(update, context, "quiz")
    await send_text(update, context, text)
    content = "Обери тему, на яку будеш грати:"
    await send_text_buttons(update, context, content, {
        "quiz_prog": "програмування мовою python",
        "quiz_math": "математичні теорії",
        "quiz_biology": "біологія",
        # "quiz_more": "питання на ту ж тему",
        "end_btn": "Закінчити"
    })


async def quiz_handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    correct_answers_count = 0
    if update.message and update.message.text:
        question = update.message.text
    else:
        question = "  "
    print("Отримано оновлення без повідомлення")
    print(f"Користувач запитав що: {question}")  # перевірка тексту запитання в терміналі
    if len(question) > 500:  # перевіряємо текст запитання на довжину
        await send_text(update, context, "Your question is too long, no more 500 characters.")
        return

## 4.1 *"Квіз"* програмування мовою python
async def quiz_prog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Ти обрав програмування мовою python, щоб почати, напиши: quiz prog"
    await send_text(update, context, text)
    load_prompt("quiz")  # завантажуємо промпт для GPT
    # # question = update.message.text
    # content = await chat_gpt.send_question(prompt, None)  # відправляємо промпт та питання до GPT
    # await send_text(update, context, content)  # Надсилання відповіді від GPT користувачу
    # # answer = await chat_gpt.send_message_list()  # отримуємо відповідь від GPT та направляємо в термінал
    # # print(f"GPT відповідає: {answer}")


dialog = Dialog()
dialog.mode = "default"


chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
app = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

# Зареєструвати обробник команди можна так:
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('quiz', quiz))

app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.add_handler(MessageHandler(filters.TEXT, quiz_handle_message))

# Зареєструвати обробник колбеку можна так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(default_callback_handler))
app.run_polling()
