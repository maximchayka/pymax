# Max Bot API Client for Python

Полнофункциональная Python-библиотека для работы с [Max Messenger Bot API](https://max.ru).

Портирована с официальной [Go-библиотеки](https://github.com/max-messenger/max-bot-api-client-go).

## Особенности

- **Синхронный и асинхронный API** — выбирайте подходящий стиль
- **Полная типизация** — Pydantic модели для всех структур данных
- **Современный HTTP-клиент** — на базе httpx с поддержкой таймаутов и retry
- **Long Polling** — простое получение обновлений в цикле
- **Webhooks** — интеграция с любым веб-фреймворком
- **Удобный API** — интуитивные методы для всех операций
- **Построитель клавиатур** — fluent-интерфейс для создания кнопок

## Установка

```bash
pip install max-bot-api
```

Или установка из исходников:

```bash
pip install git+https://github.com/max-messenger/max-bot-api-python.git
```

### Зависимости

- Python 3.10+
- httpx >= 0.25.0
- pydantic >= 2.0.0

## Быстрый старт

### Получение токена

1. Откройте Max Messenger
2. Найдите бота @MasterBot
3. Отправьте команду `/newbot`
4. Следуйте инструкциям для создания бота
5. Скопируйте полученный токен

### Минимальный бот

```python
import os
from maxbot import MaxBot, MessageCreatedUpdate

# Создаём клиент
bot = MaxBot(os.environ["MAX_BOT_TOKEN"])

# Получаем информацию о боте
info = bot.bots.get_bot()
print(f"Бот запущен: {info.name} (@{info.username})")

# Обрабатываем обновления
for update in bot.poll_updates():
    if isinstance(update, MessageCreatedUpdate):
        message = update.message
        chat_id = message.recipient.chat_id
        text = message.body.text

        if text:
            bot.messages.send(chat_id=chat_id, text=f"Вы написали: {text}")
```

## Архитектура библиотеки

### Основные классы

| Класс | Описание |
|-------|----------|
| `MaxBot` | Синхронный клиент |
| `AsyncMaxBot` | Асинхронный клиент |
| `KeyboardBuilder` | Построитель клавиатур |

### API-модули

Каждый клиент содержит модули для работы с различными сущностями:

| Модуль | Описание |
|--------|----------|
| `bot.bots` | Информация о боте |
| `bot.chats` | Управление чатами |
| `bot.messages` | Отправка и редактирование сообщений |
| `bot.subscriptions` | Webhook-подписки |
| `bot.uploads` | Загрузка файлов |

## Работа с сообщениями

### Отправка текстовых сообщений

```python
from maxbot import MaxBot

bot = MaxBot("YOUR_TOKEN")

# Отправка в чат
result = bot.messages.send(
    chat_id=123456789,
    text="Привет! Это сообщение от бота.",
)
print(f"Сообщение отправлено: {result.message.body.mid}")

# Отправка конкретному пользователю
bot.messages.send(
    user_id=987654321,
    text="Личное сообщение",
)
```

### Форматирование текста

```python
# HTML-форматирование
bot.messages.send(
    chat_id=chat_id,
    text="<b>Жирный</b>, <i>курсив</i>, <code>код</code>",
    format="html",
)

# Markdown
bot.messages.send(
    chat_id=chat_id,
    text="**Жирный**, *курсив*, `код`",
    format="markdown",
)
```

### Редактирование сообщений

```python
# Отправляем сообщение
result = bot.messages.send(chat_id=chat_id, text="Исходный текст")
message_id = result.message.body.mid

# Редактируем
bot.messages.edit_message(
    message_id=message_id,
    text="Обновлённый текст",
)
```

### Удаление сообщений

```python
bot.messages.delete_message(message_id="mid_123456")
```

### Получение сообщений

```python
# Получить сообщения из чата
messages = bot.messages.get_messages(chat_id=123456789, count=10)
for msg in messages.messages:
    print(f"{msg.sender.name}: {msg.body.text}")

# Получить конкретное сообщение
message = bot.messages.get_message(message_id="mid_123456")
```

## Клавиатуры и кнопки

### Создание инлайн-клавиатуры

```python
from maxbot import MaxBot, KeyboardBuilder

bot = MaxBot("YOUR_TOKEN")

# Создаём клавиатуру
keyboard = KeyboardBuilder()

# Добавляем кнопку с callback
keyboard.callback("Нажми меня", payload="button_clicked")

# Добавляем кнопку-ссылку
keyboard.link("Открыть сайт", url="https://max.ru")

# Несколько кнопок в одной строке
row = keyboard.add_row()
row.add_callback("Да", payload="yes", intent="positive")
row.add_callback("Нет", payload="no", intent="negative")

# Отправляем сообщение с клавиатурой
bot.messages.send(
    chat_id=chat_id,
    text="Выберите действие:",
    keyboard=keyboard,
)
```

### Типы кнопок

```python
keyboard = KeyboardBuilder()

# Callback-кнопка (отправляет событие боту)
row = keyboard.add_row()
row.add_callback(
    text="Callback",
    payload="some_data",
    intent="default",  # default, positive, negative
)

# Кнопка-ссылка
row.add_link(text="Ссылка", url="https://example.com")

# Запрос контакта пользователя
row = keyboard.add_row()
row.add_contact(text="Отправить контакт")

# Запрос геолокации
row.add_geolocation(text="Отправить локацию", quick=True)

# Открытие приложения
row = keyboard.add_row()
row.add_open_app(
    text="Открыть приложение",
    url="https://app.example.com",
    app_id="my_app",
)

# Создание чата
row.add_chat(
    text="Создать чат",
    chat_title="Новый чат",
    chat_description="Описание чата",
)
```

### Обработка нажатий на кнопки

```python
from maxbot import MaxBot, MessageCallbackUpdate, MessageCreatedUpdate

bot = MaxBot("YOUR_TOKEN")

for update in bot.poll_updates():
    # Обработка callback от кнопки
    if isinstance(update, MessageCallbackUpdate):
        callback = update.callback
        payload = callback.payload

        # Отвечаем на callback (убирает "загрузку" с кнопки)
        bot.messages.answer_on_callback(
            callback_id=callback.callback_id,
            message=f"Вы нажали: {payload}",
        )

        # Дополнительная логика по payload
        if payload == "yes":
            # Редактируем сообщение с кнопками
            if update.message:
                bot.messages.edit_message(
                    message_id=update.message.body.mid,
                    text="Вы выбрали: Да",
                )
```

## Работа с чатами

### Получение информации о чате

```python
# Информация о конкретном чате
chat = bot.chats.get_chat(chat_id=123456789)
print(f"Чат: {chat.title}")
print(f"Тип: {chat.type}")  # dialog, chat, channel
print(f"Участников: {chat.participants_count}")

# Список всех чатов бота
chats = bot.chats.get_chats(count=50)
for chat in chats.chats:
    print(f"- {chat.title} ({chat.type})")
```

### Участники чата

```python
# Получить участников
members = bot.chats.get_chat_members(chat_id=chat_id, count=100)
for member in members.members:
    role = "👑" if member.is_owner else "⭐" if member.is_admin else ""
    print(f"{role} {member.name} (@{member.username})")

# Получить только админов
admins = bot.chats.get_chat_admins(chat_id=chat_id)
for admin in admins.admins:
    print(f"Админ: {admin.name}")

# Информация о конкретных пользователях
members = bot.chats.get_specific_chat_members(
    chat_id=chat_id,
    user_ids=[111, 222, 333],
)
```

### Управление участниками

```python
# Добавить пользователей в чат
bot.chats.add_member(chat_id=chat_id, user_ids=[111, 222])

# Удалить пользователя
bot.chats.remove_member(chat_id=chat_id, user_id=333)

# Удалить и заблокировать
bot.chats.remove_member(chat_id=chat_id, user_id=333, block=True)

# Выйти из чата
bot.chats.leave_chat(chat_id=chat_id)
```

### Редактирование чата

```python
from maxbot import ChatPatch

# Изменить название
bot.chats.edit_chat(
    chat_id=chat_id,
    patch=ChatPatch(title="Новое название"),
)
```

### Действия в чате

```python
from maxbot import SenderAction

# Показать индикатор "печатает..."
bot.chats.send_action(chat_id=chat_id, action=SenderAction.TYPING_ON)

# Другие действия
bot.chats.send_action(chat_id=chat_id, action=SenderAction.SENDING_PHOTO)
bot.chats.send_action(chat_id=chat_id, action=SenderAction.SENDING_VIDEO)
bot.chats.send_action(chat_id=chat_id, action=SenderAction.SENDING_FILE)
bot.chats.send_action(chat_id=chat_id, action=SenderAction.MARK_SEEN)
```

## Загрузка и отправка файлов

### Загрузка файлов

```python
from maxbot import MaxBot

bot = MaxBot("YOUR_TOKEN")

# Загрузка фото с диска
photo = bot.uploads.upload_photo_from_file("photo.jpg")
print(f"Токен фото: {photo.token}")

# Загрузка фото по URL
photo = bot.uploads.upload_photo_from_url("https://example.com/image.jpg")

# Загрузка фото из base64
photo = bot.uploads.upload_photo_from_base64(base64_string)

# Загрузка видео
video = bot.uploads.upload_video_from_file("video.mp4")

# Загрузка аудио
audio = bot.uploads.upload_audio_from_file("audio.mp3")

# Загрузка произвольного файла
file = bot.uploads.upload_media_from_file("document.pdf")
```

### Отправка медиа

```python
from maxbot import (
    PhotoAttachmentRequest,
    PhotoAttachmentPayload,
    VideoAttachmentRequest,
    VideoAttachmentPayload,
    FileAttachmentRequest,
    FileAttachmentPayload,
)

# Загружаем и отправляем фото
photo = bot.uploads.upload_photo_from_file("photo.jpg")
bot.messages.send(
    chat_id=chat_id,
    text="Смотрите фото!",
    attachments=[
        PhotoAttachmentRequest(
            payload=PhotoAttachmentPayload(token=photo.token)
        )
    ],
)

# Отправка нескольких вложений
photo1 = bot.uploads.upload_photo_from_file("photo1.jpg")
photo2 = bot.uploads.upload_photo_from_file("photo2.jpg")
bot.messages.send(
    chat_id=chat_id,
    text="Несколько фото",
    attachments=[
        PhotoAttachmentRequest(payload=PhotoAttachmentPayload(token=photo1.token)),
        PhotoAttachmentRequest(payload=PhotoAttachmentPayload(token=photo2.token)),
    ],
)
```

### Отправка геолокации

```python
from maxbot import LocationAttachmentRequest, LocationAttachmentPayload

bot.messages.send(
    chat_id=chat_id,
    text="Моя локация",
    attachments=[
        LocationAttachmentRequest(
            payload=LocationAttachmentPayload(
                latitude=55.7558,
                longitude=37.6173,
            )
        )
    ],
)
```

## Обработка обновлений

### Типы обновлений

```python
from maxbot import (
    MaxBot,
    # Сообщения
    MessageCreatedUpdate,
    MessageEditedUpdate,
    MessageRemovedUpdate,
    MessageCallbackUpdate,
    # Бот
    BotStartedUpdate,
    BotAddedToChatUpdate,
    BotRemovedFromChatUpdate,
    # Пользователи
    UserAddedToChatUpdate,
    UserRemovedFromChatUpdate,
    # Чат
    ChatTitleChangedUpdate,
)

bot = MaxBot("YOUR_TOKEN")

for update in bot.poll_updates():
    # Новое сообщение
    if isinstance(update, MessageCreatedUpdate):
        print(f"Новое сообщение: {update.message.body.text}")

    # Сообщение отредактировано
    elif isinstance(update, MessageEditedUpdate):
        print(f"Сообщение изменено: {update.message.body.text}")

    # Сообщение удалено
    elif isinstance(update, MessageRemovedUpdate):
        print(f"Сообщение удалено: {update.message_id}")

    # Нажата кнопка
    elif isinstance(update, MessageCallbackUpdate):
        print(f"Callback: {update.callback.payload}")

    # Пользователь запустил бота (/start)
    elif isinstance(update, BotStartedUpdate):
        print(f"Пользователь {update.user.name} запустил бота")
        # Отправляем приветствие
        bot.messages.send(
            chat_id=update.chat_id,
            text=f"Привет, {update.user.name}!",
        )

    # Бота добавили в чат
    elif isinstance(update, BotAddedToChatUpdate):
        print(f"Бота добавили в чат {update.chat_id}")

    # Бота удалили из чата
    elif isinstance(update, BotRemovedFromChatUpdate):
        print(f"Бота удалили из чата {update.chat_id}")

    # Пользователь присоединился к чату
    elif isinstance(update, UserAddedToChatUpdate):
        print(f"{update.user.name} присоединился к чату")

    # Пользователь покинул чат
    elif isinstance(update, UserRemovedFromChatUpdate):
        print(f"{update.user.name} покинул чат")

    # Название чата изменено
    elif isinstance(update, ChatTitleChangedUpdate):
        print(f"Новое название чата: {update.title}")
```

### Фильтрация обновлений

```python
# Получать только определённые типы обновлений
for update in bot.poll_updates(types=["message_created", "message_callback"]):
    ...
```

### Настройки Long Polling

```python
for update in bot.poll_updates(
    limit=50,           # Максимум обновлений за запрос (до 50)
    timeout=30,         # Таймаут long polling в секундах
    max_retries=5,      # Максимум попыток при ошибке
    retry_delay=2.0,    # Начальная задержка retry (экспоненциальный backoff)
):
    ...
```

## Асинхронный API

### Базовое использование

```python
import asyncio
from maxbot import AsyncMaxBot, MessageCreatedUpdate

async def main():
    async with AsyncMaxBot("YOUR_TOKEN") as bot:
        # Получаем информацию о боте
        info = await bot.bots.get_bot()
        print(f"Бот: {info.name}")

        # Обрабатываем обновления
        async for update in bot.poll_updates():
            if isinstance(update, MessageCreatedUpdate):
                chat_id = update.message.recipient.chat_id
                text = update.message.body.text

                await bot.messages.send(
                    chat_id=chat_id,
                    text=f"Echo: {text}",
                )

asyncio.run(main())
```

### Параллельные операции

```python
import asyncio
from maxbot import AsyncMaxBot

async def main():
    async with AsyncMaxBot("YOUR_TOKEN") as bot:
        # Параллельная отправка сообщений
        await asyncio.gather(
            bot.messages.send(chat_id=111, text="Сообщение 1"),
            bot.messages.send(chat_id=222, text="Сообщение 2"),
            bot.messages.send(chat_id=333, text="Сообщение 3"),
        )

asyncio.run(main())
```

## Webhooks

### Настройка подписки

```python
# Подписка на webhook
bot.subscriptions.subscribe(
    url="https://your-domain.com/webhook",
    update_types=["message_created", "message_callback"],
    secret="optional_secret_key",
)

# Получить активные подписки
subs = bot.subscriptions.get_subscriptions()
for sub in subs.subscriptions:
    print(f"URL: {sub.url}")

# Отписаться
bot.subscriptions.unsubscribe(url="https://your-domain.com/webhook")
```

### Пример с FastAPI

```python
import os
from fastapi import FastAPI, Request
from maxbot import AsyncMaxBot, MessageCreatedUpdate

app = FastAPI()
bot = AsyncMaxBot(os.environ["MAX_BOT_TOKEN"])

@app.on_event("startup")
async def startup():
    # Регистрируем webhook при запуске
    await bot.subscriptions.subscribe(
        url="https://your-domain.com/webhook",
        update_types=["message_created", "message_callback"],
    )

    info = await bot.bots.get_bot()
    print(f"Бот запущен: {info.name}")

@app.on_event("shutdown")
async def shutdown():
    await bot.close()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = bot.handle_webhook(data)

    if isinstance(update, MessageCreatedUpdate):
        message = update.message
        chat_id = message.recipient.chat_id
        text = message.body.text

        if chat_id and text:
            await bot.messages.send(
                chat_id=chat_id,
                text=f"Получено через webhook: {text}",
            )

    return {"ok": True}

@app.get("/health")
async def health():
    return {"status": "ok"}
```

Запуск:
```bash
uvicorn webhook_bot:app --host 0.0.0.0 --port 8000
```

### Пример с Flask

```python
import os
from flask import Flask, request, jsonify
from maxbot import MaxBot, MessageCreatedUpdate

app = Flask(__name__)
bot = MaxBot(os.environ["MAX_BOT_TOKEN"])

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    update = bot.handle_webhook(data)

    if isinstance(update, MessageCreatedUpdate):
        message = update.message
        chat_id = message.recipient.chat_id
        text = message.body.text

        if chat_id and text:
            bot.messages.send(chat_id=chat_id, text=f"Echo: {text}")

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

## Управление ботом

### Информация о боте

```python
# Получить информацию
info = bot.bots.get_bot()
print(f"ID: {info.user_id}")
print(f"Имя: {info.name}")
print(f"Username: {info.username}")
print(f"Описание: {info.description}")

# Команды бота
if info.commands:
    for cmd in info.commands:
        print(f"/{cmd.name} - {cmd.description}")
```

### Редактирование бота

```python
from maxbot import BotPatch, BotCommand

# Обновить информацию о боте
bot.bots.patch_bot(BotPatch(
    name="Новое имя бота",
    description="Новое описание бота",
    commands=[
        BotCommand(name="start", description="Запустить бота"),
        BotCommand(name="help", description="Показать справку"),
        BotCommand(name="settings", description="Настройки"),
    ],
))
```

## Обработка ошибок

```python
from maxbot import (
    MaxBot,
    MaxBotError,
    APIError,
    NetworkError,
    TimeoutError,
    EmptyTokenError,
)

try:
    bot = MaxBot("YOUR_TOKEN")
    bot.messages.send(chat_id=123, text="Hello")

except EmptyTokenError:
    print("Токен не указан!")

except APIError as e:
    print(f"Ошибка API [{e.code}]: {e.message}")
    if e.details:
        print(f"Детали: {e.details}")

except NetworkError as e:
    print(f"Сетевая ошибка: {e}")

except TimeoutError as e:
    print(f"Таймаут: {e}")

except MaxBotError as e:
    print(f"Ошибка бота: {e}")
```

## Полные примеры

### Эхо-бот с командами

```python
import os
from maxbot import MaxBot, MessageCreatedUpdate, KeyboardBuilder

def main():
    bot = MaxBot(os.environ["MAX_BOT_TOKEN"])

    info = bot.bots.get_bot()
    print(f"Бот запущен: {info.name}")

    for update in bot.poll_updates():
        if not isinstance(update, MessageCreatedUpdate):
            continue

        message = update.message
        chat_id = message.recipient.chat_id if message.recipient else None
        text = message.body.text or ""

        if not chat_id:
            continue

        if text == "/start":
            keyboard = KeyboardBuilder()
            keyboard.callback("📚 Помощь", "help")
            keyboard.callback("ℹ️ О боте", "about")

            bot.messages.send(
                chat_id=chat_id,
                text=f"Привет, {message.sender.name}! 👋\n\n"
                     f"Я эхо-бот. Отправь мне любое сообщение, "
                     f"и я повторю его.",
                keyboard=keyboard,
            )

        elif text == "/help":
            bot.messages.send(
                chat_id=chat_id,
                text="📚 <b>Команды:</b>\n\n"
                     "/start - Начать работу\n"
                     "/help - Показать справку\n"
                     "/about - О боте",
                format="html",
            )

        elif text == "/about":
            bot.messages.send(
                chat_id=chat_id,
                text="ℹ️ <b>Эхо-бот</b>\n\n"
                     "Версия: 1.0.0\n"
                     "Создан с помощью max-bot-api",
                format="html",
            )

        elif text.startswith("/"):
            bot.messages.send(
                chat_id=chat_id,
                text="❌ Неизвестная команда. Введите /help для справки.",
            )

        else:
            bot.messages.send(
                chat_id=chat_id,
                text=f"🔄 {text}",
            )

if __name__ == "__main__":
    main()
```

### Бот-счётчик с кнопками

```python
import asyncio
import os
from maxbot import (
    AsyncMaxBot,
    MessageCreatedUpdate,
    MessageCallbackUpdate,
    KeyboardBuilder,
)

async def main():
    async with AsyncMaxBot(os.environ["MAX_BOT_TOKEN"]) as bot:
        info = await bot.bots.get_bot()
        print(f"Бот запущен: {info.name}")

        async for update in bot.poll_updates():
            if isinstance(update, MessageCreatedUpdate):
                await handle_message(bot, update)
            elif isinstance(update, MessageCallbackUpdate):
                await handle_callback(bot, update)

async def handle_message(bot: AsyncMaxBot, update: MessageCreatedUpdate):
    message = update.message
    chat_id = message.recipient.chat_id if message.recipient else None
    text = message.body.text or ""

    if not chat_id:
        return

    if text == "/start":
        keyboard = KeyboardBuilder()

        row = keyboard.add_row()
        row.add_callback("📊 Счётчик: 0", "show:0")

        row = keyboard.add_row()
        row.add_callback("➕", "add:1", intent="positive")
        row.add_callback("➖", "sub:1", intent="negative")

        row = keyboard.add_row()
        row.add_callback("🔄 Сброс", "reset")

        await bot.messages.send(
            chat_id=chat_id,
            text="🔢 <b>Счётчик</b>\n\nНажимайте кнопки для изменения значения.",
            format="html",
            keyboard=keyboard,
        )

async def handle_callback(bot: AsyncMaxBot, update: MessageCallbackUpdate):
    callback = update.callback
    payload = callback.payload or ""
    message = update.message

    if not message:
        await bot.messages.answer_on_callback(callback.callback_id)
        return

    # Извлекаем текущее значение из первой кнопки
    current = 0
    if message.body.attachments:
        for att in message.body.attachments:
            if att.type == "inline_keyboard" and att.payload.buttons:
                first_row = att.payload.buttons[0]
                if first_row:
                    btn = first_row[0]
                    if hasattr(btn, "payload") and btn.payload:
                        try:
                            current = int(btn.payload.split(":")[1])
                        except (IndexError, ValueError):
                            pass
                break

    # Обрабатываем действие
    if payload.startswith("add:"):
        delta = int(payload.split(":")[1])
        current += delta
    elif payload.startswith("sub:"):
        delta = int(payload.split(":")[1])
        current -= delta
    elif payload == "reset":
        current = 0
    elif payload.startswith("show:"):
        await bot.messages.answer_on_callback(
            callback.callback_id,
            message=f"Текущее значение: {current}",
        )
        return

    # Обновляем клавиатуру
    keyboard = KeyboardBuilder()

    row = keyboard.add_row()
    row.add_callback(f"📊 Счётчик: {current}", f"show:{current}")

    row = keyboard.add_row()
    row.add_callback("➕", "add:1", intent="positive")
    row.add_callback("➖", "sub:1", intent="negative")

    row = keyboard.add_row()
    row.add_callback("🔄 Сброс", "reset")

    await bot.messages.edit_message(
        message_id=message.body.mid,
        text=f"🔢 <b>Счётчик</b>\n\nТекущее значение: <code>{current}</code>",
        format="html",
        keyboard=keyboard,
    )

    await bot.messages.answer_on_callback(callback.callback_id)

if __name__ == "__main__":
    asyncio.run(main())
```

## Структура проекта

```
maxbot/
├── __init__.py          # Публичный API
├── api.py               # MaxBot и AsyncMaxBot
├── client.py            # HTTP-клиенты
├── errors.py            # Исключения
├── bots.py              # API ботов
├── chats.py             # API чатов
├── messages.py          # API сообщений
├── subscriptions.py     # API подписок
├── uploads.py           # API загрузки файлов
├── keyboard.py          # Построитель клавиатур
├── py.typed             # Маркер типизации
└── schemes/
    ├── __init__.py
    └── models.py        # Pydantic-модели
```

## Разработка

### Установка зависимостей разработки

```bash
pip install -e ".[dev]"
```

### Запуск тестов

```bash
pytest
```

### Проверка типов

```bash
mypy maxbot
```

### Линтер

```bash
ruff check .
ruff format .
```

## Лицензия

MIT License

## Ссылки

- [Max Messenger](https://max.ru)
- [Go-библиотека (оригинал)](https://github.com/max-messenger/max-bot-api-client-go)
- [Документация API](https://max.ru/dev)
