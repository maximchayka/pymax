# Max Bot API Client for Python

Python client library for [Max Messenger Bot API](https://max.ru).

Ported from the official [Go client](https://github.com/max-messenger/max-bot-api-client-go).

## Installation

```bash
pip install max-bot-api
```

Or install from source:

```bash
pip install git+https://github.com/max-messenger/max-bot-api-python.git
```

## Quick Start

### Simple Echo Bot

```python
from maxbot import MaxBot, MessageCreatedUpdate

bot = MaxBot("YOUR_BOT_TOKEN")

# Get bot info
info = bot.bots.get_bot()
print(f"Bot: {info.name}")

# Poll for updates
for update in bot.poll_updates():
    if isinstance(update, MessageCreatedUpdate):
        message = update.message
        chat_id = message.recipient.chat_id
        text = message.body.text

        # Echo the message
        bot.messages.send(chat_id=chat_id, text=f"You said: {text}")
```

### Async Bot

```python
import asyncio
from maxbot import AsyncMaxBot, MessageCreatedUpdate

async def main():
    async with AsyncMaxBot("YOUR_BOT_TOKEN") as bot:
        async for update in bot.poll_updates():
            if isinstance(update, MessageCreatedUpdate):
                message = update.message
                chat_id = message.recipient.chat_id
                text = message.body.text

                await bot.messages.send(chat_id=chat_id, text=f"Echo: {text}")

asyncio.run(main())
```

### Using Keyboards

```python
from maxbot import MaxBot, KeyboardBuilder

bot = MaxBot("YOUR_BOT_TOKEN")

# Create inline keyboard
keyboard = KeyboardBuilder()

# Add single button per row
keyboard.callback("Click me!", "button_clicked")
keyboard.link("Visit website", "https://max.ru")

# Add multiple buttons in a row
row = keyboard.add_row()
row.add_callback("Yes", "yes", intent="positive")
row.add_callback("No", "no", intent="negative")

# Send message with keyboard
bot.messages.send(
    chat_id=123456789,
    text="Choose an option:",
    keyboard=keyboard,
)
```

### Handling Callbacks

```python
from maxbot import MaxBot, MessageCallbackUpdate

for update in bot.poll_updates():
    if isinstance(update, MessageCallbackUpdate):
        callback = update.callback

        # Answer the callback
        bot.messages.answer_on_callback(
            callback_id=callback.callback_id,
            message="Button clicked!",
        )
```

### Uploading Files

```python
from maxbot import MaxBot, PhotoAttachmentRequest, PhotoAttachmentPayload

bot = MaxBot("YOUR_BOT_TOKEN")

# Upload photo from file
uploaded = bot.uploads.upload_photo_from_file("photo.jpg")

# Send message with photo
bot.messages.send(
    chat_id=123456789,
    text="Here's a photo!",
    attachments=[
        PhotoAttachmentRequest(
            payload=PhotoAttachmentPayload(token=uploaded.token)
        )
    ],
)
```

### Working with Chats

```python
# Get chat info
chat = bot.chats.get_chat(chat_id=123456789)
print(f"Chat: {chat.title}")

# Get chat members
members = bot.chats.get_chat_members(chat_id=123456789)
for member in members.members:
    print(f"Member: {member.name}")

# Send typing indicator
from maxbot import SenderAction
bot.chats.send_action(chat_id=123456789, action=SenderAction.TYPING_ON)
```

### Webhook Mode

```python
from fastapi import FastAPI, Request
from maxbot import AsyncMaxBot, MessageCreatedUpdate

app = FastAPI()
bot = AsyncMaxBot("YOUR_BOT_TOKEN")

@app.on_event("startup")
async def startup():
    await bot.subscriptions.subscribe(
        url="https://your-domain.com/webhook",
        update_types=["message_created"],
    )

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = bot.handle_webhook(data)

    if isinstance(update, MessageCreatedUpdate):
        # Handle message...
        pass

    return {"ok": True}
```

## API Reference

### Main Classes

- `MaxBot` - Sync bot client
- `AsyncMaxBot` - Async bot client
- `KeyboardBuilder` - Inline keyboard builder

### API Modules

- `bot.bots` - Bot info management
- `bot.chats` - Chat management
- `bot.messages` - Message sending/editing
- `bot.subscriptions` - Webhook subscriptions
- `bot.uploads` - File uploads

### Update Types

- `MessageCreatedUpdate` - New message received
- `MessageEditedUpdate` - Message was edited
- `MessageRemovedUpdate` - Message was deleted
- `MessageCallbackUpdate` - Callback button clicked
- `BotStartedUpdate` - User started the bot
- `BotAddedToChatUpdate` - Bot added to chat
- `BotRemovedFromChatUpdate` - Bot removed from chat
- `UserAddedToChatUpdate` - User joined chat
- `UserRemovedFromChatUpdate` - User left chat
- `ChatTitleChangedUpdate` - Chat title changed

## Examples

See the [examples](examples/) directory for more examples:

- [Simple bot](examples/simple_bot.py) - Basic echo bot
- [Async bot](examples/async_bot.py) - Async bot with callbacks
- [Webhook bot](examples/webhook_bot.py) - FastAPI webhook example

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linter:

```bash
ruff check .
```

Type checking:

```bash
mypy maxbot
```

## License

MIT License
