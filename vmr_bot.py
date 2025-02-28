import os
import asyncio
import subprocess
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from vosk import Model, KaldiRecognizer, SetLogLevel
from dotenv import load_dotenv

# Отключаем логирование Vosk при необходимости
# SetLogLevel(-1)

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка наличия токена
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Необходимо указать TELEGRAM_BOT_TOKEN в файле .env")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Загрузка моделей Vosk
models = {
    "en": Model("vosk-model-small-en-us-0.15"),
    "ru": Model("vosk-model-small-ru-0.4"),
    "es": Model("vosk-model-small-es-0.42")
}

# Доступные языки с эмодзи
available_languages = {
    "en": "🇺🇸 Английский",
    "ru": "🇷🇺 Русский",
    "es": "🇪🇸 Испанский"
}

# Отслеживание пользователей, которым отправлено приветствие
user_greetings = set()

# Функция для конвертации аудио в PCM 16kHz
def convert_audio(audio_bytes):
    process = subprocess.Popen(
        [
            "ffmpeg", "-i", "pipe:0",
            "-ar", "16000",
            "-ac", "1",
            "-f", "s16le",
            "-"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    pcm_data, _ = process.communicate(audio_bytes)
    return pcm_data

# Функция для распознавания аудио и получения доверия
def recognize_audio(pcm_data, model):
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    recognizer.AcceptWaveform(pcm_data)
    result = json.loads(recognizer.FinalResult())
    text = result.get('text', '')
    confidence = 0.0
    words = result.get('result', [])
    if words:
        confidences = [word.get('conf', 0.0) for word in words]
        confidence = sum(confidences) / len(confidences)
    return text, confidence

# Функция для отправки приветственного сообщения
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Привет!\n\n"
        "Я 🤖 *Speech-to-Text Bot*, и я могу преобразовывать твои голосовые сообщения в текст на нескольких языках! /languages 🌐\n\n"
        "📩 Просто отправь мне голосовое сообщение, и я распознаю его содержимое.\n\n"
        "☝️ Поскольку я пока в стадии 🩼бета-тестирования🩼, постарайся отправлять сообщения от 2 секунд.\n"
        "Хотя я иногда неплохо справляюсь и с более короткими сообщениями 💪, но это как повезет...🤷‍♂️\n\n"
        "Чтобы узнать больше о моих возможностях, введи команду /help или /about."
    "Hello! \n\n"
    "I am 🤖 *Speech-to-Text Bot *, and I can convert your voice messages into text in several /languages 🌐 \n\n"
    "📩 Just send me a voice message, and I will recognize its contents.\n\n"
    "☝️ Since I am still in the stage of 🩼Beta🩼testing🩼, please try to send messages from 2 seconds length.\n"
    "Although I sometimes cope well with shorter messages 💪, but it's like luck ... 🤷Sometimes...\n\n"
    "To learn more about my possibilities, enter the team /help or /about."
        ,
        parse_mode="Markdown"
    )

# Обработчик команды /start
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_greetings.add(user_id)
    await send_welcome(message)

# Обработчик команды /help
async def help_command(message: types.Message):
    await message.reply(
        "❓ *Помощь*\n\n"
        "Я могу распознавать голосовые сообщения на следующих языках:\n"
        f"{', '.join(available_languages.values())}\n\n"
        "📚 *Доступные команды:*\n"
        "/start - Приветственное сообщение\n"
        "/help - Показать это сообщение помощи\n"
        "/languages - Показать доступные языки распознавания\n"
        "/about - Информация обо мне\n"
        "/changelog - Последние изменения\n"
        "/restart - Перезагрузить модели распознавания\n"
        
        "❓ *Help: *\n\n"
        "I can recognize voice messages in the following languages: \n\n"
        "📚 *Available commands: *\n"
        "/start - welcome message \n"
        "/help - Show this Message of Assistance \n"
        "/languages - Show affordable recognition languages \n"
        "/about - Information about me \n"
        "/changelog - recent changes \n"
        "/restart - restart recognition models"
        ,
        parse_mode="Markdown"
    )

# Обработчик команды /languages
async def languages_command(message: types.Message):
    languages_text = "🌐 *Доступные языки распознавания:*\n\n"
    for code, lang in available_languages.items():
        languages_text += f"{lang} (`{code}`)\n"
    await message.reply(languages_text, parse_mode="Markdown")

# Обработчик команды /about
async def about_command(message: types.Message):
    await message.reply(
        "ℹ️ *Обо мне*\n\n"
        "Я 🤖 *Speech-to-Text Bot*, созданный для преобразования твоих голосовых сообщений в текст.\n\n"
        "💡 *Технологии:*\n"
        "- Использую библиотеку *Vosk* для офлайн-распознавания речи.\n"
        "- Код на *Python* с использованием *aiogram* для взаимодействия с Telegram API.\n\n"
        "👨‍💻 Если у тебя есть вопросы или предложения, пожалуйста, свяжись со мной!\n\n"
        "Например, напиши мне на dm.ilyushko@gmail.com или найди меня здесь: https://github.com/lightclove\n\n"
        "Надеюсь, бот тебе понравится и будет полезен! В любом случае, он постоянно обновляется\n\n"
        "и в него добавляются новые фичи и возможности: `/changelog` \n\n"
        
        "I am 🤖 Speech-to-Text Bot, and I can convert your voice messages into text in several /languages 🌐\n\n"
        "📩 Just send me a voice message, and I recognize its contents.\n\n"
        "☝️ Since I am still in the stage of 🩼Bet testing🩼, try to send messages from 2 seconds.\n\n"
        "Although I sometimes cope well with shorter messages 💪, but it's like luck ... 🤷‍♂️\n\n"
        "To learn more about my capabilities, enter the team /help or /about.\n\n",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# Обработчик команды /changelog
async def changelog_command(message: types.Message):
    await message.reply(
        "📝 *Последние изменения:*\n\n"
        "- Добавлена команда `/changelog` для отображения изменений.\n"
        "- Улучшено распознавание коротких сообщений.\n"
        "- Исправлены ошибки и повышена стабильность.\n"
        "- Добавлены новые команды и эмодзи для удобства.\n\n"

        "📝 *last changes *\n\n"
        "- added the `/changelog` team to display changes. \n"
        "- Improved short messages.\n"
        "- Fixed errors and increased stability.\n"
        "- added new teams and emoji for convenience.\n\n"
        ,
        parse_mode="Markdown"
    )

# Обработчик команды /restart
async def restart_command(message: types.Message):
    global models
    models = {
        "en": Model("vosk-model-small-en-us-0.15"),
        "ru": Model("vosk-model-small-ru-0.4"),
        "es": Model("vosk-model-small-es-0.42")
    }
    await message.reply("🔄 *Модели распознавания были перезагружены.*", parse_mode="Markdown")

# Обработчик голосовых сообщений
async def handle_voice_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_greetings:
        user_greetings.add(user_id)
        await send_welcome(message)

    voice = message.voice
    voice_file = await bot.get_file(voice.file_id)
    voice_bytes = await bot.download_file(voice_file.file_path)
    audio_bytes = voice_bytes.read()

    # Конвертация аудио
    pcm_data = convert_audio(audio_bytes)

    texts = {}
    confidences = {}

    # Распознавание с каждой моделью
    for lang_code, model in models.items():
        text, confidence = recognize_audio(pcm_data, model)
        texts[lang_code] = text
        confidences[lang_code] = confidence
        print(f"Модель: {lang_code}, Доверие: {confidence}, Текст: {text}")

    # Выбор лучшей модели
    best_lang = max(confidences, key=confidences.get)
    best_text = texts[best_lang]

    # Отправка результата
    await message.reply(
        f"🔎 *Распознано сообщение:*\n\n"
        f"🌐 Язык: {available_languages[best_lang]}\n"
        f"📝 Текст: {best_text}",
        parse_mode="Markdown"
    )

# Обработчик текстовых сообщений
async def handle_text_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_greetings:
        user_greetings.add(user_id)
        await send_welcome(message)

    await message.reply(
        "⚠️ Пожалуйста, отправь мне голосовое сообщение для распознавания.\n"
        "Для получения помощи введи /help"
    )

# Регистрация обработчиков
dp.message.register(start_command, Command(commands=["start"]))
dp.message.register(help_command, Command(commands=["help"]))
dp.message.register(languages_command, Command(commands=["languages"]))
dp.message.register(about_command, Command(commands=["about"]))
dp.message.register(changelog_command, Command(commands=["changelog"]))
dp.message.register(restart_command, Command(commands=["restart"]))
dp.message.register(handle_voice_message, F.voice)
dp.message.register(handle_text_message, F.text & ~F.text.startswith('/'))

# Запуск бота
async def main():
    print("🤖 Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
