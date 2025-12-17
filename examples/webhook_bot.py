"""Webhook bot example using FastAPI."""

import os

# Note: Install with `pip install fastapi uvicorn`
try:
    from fastapi import FastAPI, Request
    import uvicorn
except ImportError:
    print("Please install fastapi and uvicorn: pip install fastapi uvicorn")
    exit(1)

from maxbot import AsyncMaxBot, MessageCreatedUpdate


app = FastAPI()
bot: AsyncMaxBot | None = None


@app.on_event("startup")
async def startup() -> None:
    """Initialize bot on startup."""
    global bot

    token = os.environ.get("MAX_BOT_TOKEN")
    if not token:
        raise ValueError("MAX_BOT_TOKEN environment variable is required")

    bot = AsyncMaxBot(token)

    # Get webhook URL from environment or use default
    webhook_url = os.environ.get("WEBHOOK_URL", "https://your-domain.com/webhook")

    # Subscribe to webhook
    await bot.subscriptions.subscribe(
        url=webhook_url,
        update_types=["message_created", "message_callback"],
    )

    bot_info = await bot.bots.get_bot()
    print(f"Bot started: {bot_info.name}")
    print(f"Webhook URL: {webhook_url}")


@app.on_event("shutdown")
async def shutdown() -> None:
    """Cleanup on shutdown."""
    global bot
    if bot:
        await bot.close()


@app.post("/webhook")
async def webhook(request: Request) -> dict:
    """Handle incoming webhook updates."""
    global bot
    if not bot:
        return {"ok": False, "error": "Bot not initialized"}

    # Parse update data
    data = await request.json()
    update = bot.handle_webhook(data)

    # Handle message updates
    if isinstance(update, MessageCreatedUpdate):
        message = update.message
        chat_id = message.recipient.chat_id if message.recipient else None
        text = message.body.text

        if chat_id and text:
            # Simple echo response
            await bot.messages.send(
                chat_id=chat_id,
                text=f"Webhook received: {text}",
            )

    return {"ok": True}


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
