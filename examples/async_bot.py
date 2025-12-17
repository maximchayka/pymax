"""Async bot example with callback handling."""

import asyncio
import os

from maxbot import (
    AsyncMaxBot,
    KeyboardBuilder,
    MessageCallbackUpdate,
    MessageCreatedUpdate,
)


async def main() -> None:
    # Get token from environment
    token = os.environ.get("MAX_BOT_TOKEN")
    if not token:
        print("Please set MAX_BOT_TOKEN environment variable")
        return

    # Create async bot instance
    async with AsyncMaxBot(token) as bot:
        # Get bot info
        bot_info = await bot.bots.get_bot()
        print(f"Bot started: {bot_info.name} (@{bot_info.username})")

        # Start polling
        print("Listening for updates...")
        try:
            async for update in bot.poll_updates():
                # Handle new messages
                if isinstance(update, MessageCreatedUpdate):
                    await handle_message(bot, update)

                # Handle callback buttons
                elif isinstance(update, MessageCallbackUpdate):
                    await handle_callback(bot, update)

        except asyncio.CancelledError:
            print("\nStopping bot...")
            bot.stop_polling()


async def handle_message(bot: AsyncMaxBot, update: MessageCreatedUpdate) -> None:
    """Handle incoming messages."""
    message = update.message
    chat_id = message.recipient.chat_id if message.recipient else None
    text = message.body.text

    if not chat_id or not text:
        return

    print(f"Received message: {text}")

    if text == "/start":
        # Create keyboard with buttons
        keyboard = KeyboardBuilder()
        row = keyboard.add_row()
        row.add_callback("Counter: 0", "counter:0")

        row2 = keyboard.add_row()
        row2.add_callback("+1", "add:1", intent="positive")
        row2.add_callback("-1", "add:-1", intent="negative")
        row2.add_callback("Reset", "reset")

        await bot.messages.send(
            chat_id=chat_id,
            text="Welcome! This is an interactive counter bot.\n\nClick the buttons below:",
            keyboard=keyboard,
        )

    elif text == "/help":
        await bot.messages.send(
            chat_id=chat_id,
            text="Available commands:\n"
            "/start - Start the counter\n"
            "/help - Show this help\n"
            "/keyboard - Show inline keyboard example",
        )

    elif text == "/keyboard":
        keyboard = KeyboardBuilder()
        keyboard.callback("Button 1", "btn:1")
        keyboard.link("Visit Website", "https://max.ru")

        row = keyboard.add_row()
        row.add_contact("Share Contact")
        row.add_geolocation("Share Location")

        await bot.messages.send(
            chat_id=chat_id,
            text="Here's an example keyboard:",
            keyboard=keyboard,
        )

    else:
        await bot.messages.send(
            chat_id=chat_id,
            text=f"Echo: {text}",
        )


async def handle_callback(bot: AsyncMaxBot, update: MessageCallbackUpdate) -> None:
    """Handle callback button clicks."""
    callback = update.callback
    payload = callback.payload or ""
    message = update.message

    print(f"Received callback: {payload}")

    if not message:
        await bot.messages.answer_on_callback(callback.callback_id, "No message found")
        return

    message_id = message.body.mid

    if payload.startswith("counter:"):
        # Just show current value
        current = int(payload.split(":")[1])
        await bot.messages.answer_on_callback(callback.callback_id, f"Current value: {current}")

    elif payload.startswith("add:"):
        # Extract current counter from message
        current = 0
        if message.body.attachments:
            for att in message.body.attachments:
                if att.type == "inline_keyboard":
                    buttons = att.payload.buttons
                    if buttons and buttons[0]:
                        first_button = buttons[0][0]
                        if hasattr(first_button, "payload") and first_button.payload:
                            current = int(first_button.payload.split(":")[1])
                    break

        # Update counter
        delta = int(payload.split(":")[1])
        new_value = current + delta

        # Update keyboard
        keyboard = KeyboardBuilder()
        row = keyboard.add_row()
        row.add_callback(f"Counter: {new_value}", f"counter:{new_value}")

        row2 = keyboard.add_row()
        row2.add_callback("+1", "add:1", intent="positive")
        row2.add_callback("-1", "add:-1", intent="negative")
        row2.add_callback("Reset", "reset")

        await bot.messages.edit_message(
            message_id=message_id,
            text=f"Counter updated!\n\nCurrent value: {new_value}",
            keyboard=keyboard,
        )
        await bot.messages.answer_on_callback(callback.callback_id, f"Updated to {new_value}")

    elif payload == "reset":
        keyboard = KeyboardBuilder()
        row = keyboard.add_row()
        row.add_callback("Counter: 0", "counter:0")

        row2 = keyboard.add_row()
        row2.add_callback("+1", "add:1", intent="positive")
        row2.add_callback("-1", "add:-1", intent="negative")
        row2.add_callback("Reset", "reset")

        await bot.messages.edit_message(
            message_id=message_id,
            text="Counter reset!\n\nCurrent value: 0",
            keyboard=keyboard,
        )
        await bot.messages.answer_on_callback(callback.callback_id, "Counter reset to 0")

    else:
        await bot.messages.answer_on_callback(callback.callback_id, f"Button clicked: {payload}")


if __name__ == "__main__":
    asyncio.run(main())
