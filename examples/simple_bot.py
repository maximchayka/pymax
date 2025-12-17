"""Simple echo bot example."""

import os

from maxbot import KeyboardBuilder, MaxBot, MessageCreatedUpdate


def main() -> None:
    # Get token from environment
    token = os.environ.get("MAX_BOT_TOKEN")
    if not token:
        print("Please set MAX_BOT_TOKEN environment variable")
        return

    # Create bot instance
    bot = MaxBot(token)

    # Get bot info
    bot_info = bot.bots.get_bot()
    print(f"Bot started: {bot_info.name} (@{bot_info.username})")

    # Start polling
    print("Listening for updates...")
    try:
        for update in bot.poll_updates():
            # Handle new messages
            if isinstance(update, MessageCreatedUpdate):
                message = update.message
                chat_id = message.recipient.chat_id if message.recipient else None
                text = message.body.text

                if not chat_id or not text:
                    continue

                print(f"Received message: {text}")

                # Echo the message back
                if text == "/start":
                    # Send welcome message with keyboard
                    keyboard = KeyboardBuilder()
                    keyboard.callback("Help", "help")
                    keyboard.callback("About", "about")

                    bot.messages.send(
                        chat_id=chat_id,
                        text="Welcome! I'm an echo bot.\n\nSend me any message and I'll repeat it.",
                        keyboard=keyboard,
                    )
                elif text == "/help":
                    bot.messages.send(
                        chat_id=chat_id,
                        text="Available commands:\n/start - Start the bot\n/help - Show this help",
                    )
                else:
                    # Echo the message
                    bot.messages.send(
                        chat_id=chat_id,
                        text=f"You said: {text}",
                    )

    except KeyboardInterrupt:
        print("\nStopping bot...")
        bot.stop_polling()
    finally:
        bot.close()


if __name__ == "__main__":
    main()
