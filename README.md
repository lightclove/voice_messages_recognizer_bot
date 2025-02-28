# voice_messages_recognizer_bot
Telegram voice messages recognizer bot (Transcibator) based on Vosk and aiogram, no external APIs like Google Cloun or Yandex Speechkit usage!
# 🤖 Speech-to-Text Bot

## Описание проекта
**Speech-to-Text Bot** - это Telegram-бот, который преобразует голосовые сообщения в текст на нескольких языках. Этот бот разработан как упрощенный MVP (Minimal Viable Product) и не включает обработку исключений и другие более сложные аспекты разработки. Основная цель - продемонстрировать базовую функциональность распознавания речи с использованием библиотек Vosk и aiogram.

## Функциональность
- Распознавание голосовых сообщений на английском, русском и испанском языках.
- Автоматическое определение языка сообщения на основе содержания.
- Команды для получения информации о боте и его возможностях.

## Технологии
- **Vosk**: библиотека для офлайн-распознавания речи.
- **Python**: язык программирования.
- **aiogram**: библиотека для работы с Telegram Bot API.
- **ffmpeg**: инструмент для конвертации аудио файлов.

## Требования
- Python 3.8+
- ffmpeg
- Модели Vosk для английского, русского и испанского языков:
  - [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
  - [vosk-model-small-ru-0.4](https://alphacephei.com/vosk/models/vosk-model-small-ru-0.4.zip)
  - [vosk-model-small-es-0.42](https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip)

## Запуск бота
0. Установите зависимости: vosk, aiogram, dotenv
1. Убедитесь, что ffmpeg установлен и доступен из командной строки:
```bash
ffmpeg -version
```
2. Скачайте и распакуйте модели Vosk в соответствующие директории отсюда : https://alphacephei.com/vosk/models :
  - vosk-model-small-en-us-0.15
  - vosk-model-small-ru-0.4
  - vosk-model-small-es-0.42   

3. Создайте файл .env в корневой директории проекта и добавьте в него токен вашего бота:
```bash
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_ТЕЛЕГРАМ_БОТА
```
4. Запустите скрипт бота в venv или локально(не рекомендуется)

## Доступные команды
```bash
    /start - Приветственное сообщение
    /help - Показать это сообщение помощи
    /languages - Показать доступные языки распознавания
    /about - Информация обо мне
    /changelog - Последние изменения
    /restart - Перезагрузить модели распознавания
```
