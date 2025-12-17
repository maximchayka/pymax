"""Main API class for Max Bot."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import AsyncIterator, Callable, Iterator

from maxbot.bots import AsyncBots, Bots
from maxbot.chats import AsyncChats, Chats
from maxbot.client import AsyncClient, Client, DEFAULT_API_URL, DEFAULT_TIMEOUT
from maxbot.messages import AsyncMessages, Messages
from maxbot.schemes import (
    BotAddedToChatUpdate,
    BotRemovedFromChatUpdate,
    BotStartedUpdate,
    ChatTitleChangedUpdate,
    MessageCallbackUpdate,
    MessageChatCreatedUpdate,
    MessageConstructedUpdate,
    MessageCreatedUpdate,
    MessageEditedUpdate,
    MessageRemovedUpdate,
    Update,
    UpdateList,
    UpdateType,
    UserAddedToChatUpdate,
    UserRemovedFromChatUpdate,
)
from maxbot.subscriptions import AsyncSubscriptions, Subscriptions
from maxbot.uploads import AsyncUploads, Uploads

logger = logging.getLogger(__name__)

# Update type mapping
UPDATE_TYPE_MAP: dict[str, type[Update]] = {
    "message_created": MessageCreatedUpdate,
    "message_edited": MessageEditedUpdate,
    "message_removed": MessageRemovedUpdate,
    "message_callback": MessageCallbackUpdate,
    "message_chat_created": MessageChatCreatedUpdate,
    "message_constructed": MessageConstructedUpdate,
    "bot_added": BotAddedToChatUpdate,
    "bot_removed": BotRemovedFromChatUpdate,
    "bot_started": BotStartedUpdate,
    "user_added": UserAddedToChatUpdate,
    "user_removed": UserRemovedFromChatUpdate,
    "chat_title_changed": ChatTitleChangedUpdate,
}


def _parse_update(data: dict) -> UpdateType:
    """Parse update data into appropriate update type.

    Args:
        data: Raw update data

    Returns:
        Typed update object
    """
    update_type = data.get("update_type", "")
    model_class = UPDATE_TYPE_MAP.get(update_type, Update)
    return model_class.model_validate(data)


class MaxBot:
    """Main Max Bot API client.

    This class provides access to all bot API methods and
    supports both long polling and webhook modes.
    """

    def __init__(
        self,
        token: str,
        api_url: str = DEFAULT_API_URL,
        api_version: str = "0.1.2",
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the bot.

        Args:
            token: Bot API token
            api_url: Base API URL
            api_version: API version
            timeout: Request timeout in seconds
        """
        self._client = Client(
            token=token,
            api_url=api_url,
            api_version=api_version,
            timeout=timeout,
        )

        # Initialize API modules
        self.bots = Bots(self._client)
        self.chats = Chats(self._client)
        self.messages = Messages(self._client)
        self.subscriptions = Subscriptions(self._client)
        self.uploads = Uploads(self._client)

        # Internal state
        self._marker: int | None = None
        self._running = False

    def close(self) -> None:
        """Close the bot client."""
        self._client.close()

    def __enter__(self) -> "MaxBot":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def get_updates(
        self,
        limit: int = 50,
        timeout: int = 30,
        marker: int | None = None,
        types: list[str] | None = None,
    ) -> UpdateList:
        """Get updates (long polling).

        Args:
            limit: Maximum number of updates to receive
            timeout: Long polling timeout in seconds
            marker: Update marker for pagination
            types: Types of updates to receive

        Returns:
            List of updates
        """
        params = {
            "limit": min(limit, 50),
            "timeout": timeout,
        }
        if marker is not None:
            params["marker"] = marker
        if types:
            params["types"] = ",".join(types)

        return self._client.request_model("GET", "updates", UpdateList, params=params)

    def poll_updates(
        self,
        limit: int = 50,
        timeout: int = 30,
        types: list[str] | None = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> Iterator[UpdateType]:
        """Poll for updates continuously.

        Args:
            limit: Maximum number of updates per request
            timeout: Long polling timeout in seconds
            types: Types of updates to receive
            max_retries: Maximum retry attempts on error
            retry_delay: Initial delay between retries (exponential backoff)

        Yields:
            Update objects
        """
        self._running = True
        retry_count = 0

        while self._running:
            try:
                updates = self.get_updates(
                    limit=limit,
                    timeout=timeout,
                    marker=self._marker,
                    types=types,
                )

                # Reset retry count on success
                retry_count = 0

                # Update marker for next request
                if updates.marker is not None:
                    self._marker = updates.marker

                # Yield parsed updates
                for update in updates.updates:
                    if not self._running:
                        break
                    yield update

            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error(f"Max retries reached, stopping: {e}")
                    self._running = False
                    raise

                # Exponential backoff
                delay = retry_delay * (2 ** (retry_count - 1))
                logger.warning(f"Error polling updates, retrying in {delay}s: {e}")
                time.sleep(delay)

    def stop_polling(self) -> None:
        """Stop the polling loop."""
        self._running = False

    def handle_webhook(self, data: dict) -> UpdateType:
        """Handle incoming webhook data.

        Args:
            data: Raw webhook data

        Returns:
            Parsed update object
        """
        return _parse_update(data)


class AsyncMaxBot:
    """Async Max Bot API client.

    This class provides async access to all bot API methods.
    """

    def __init__(
        self,
        token: str,
        api_url: str = DEFAULT_API_URL,
        api_version: str = "0.1.2",
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the async bot.

        Args:
            token: Bot API token
            api_url: Base API URL
            api_version: API version
            timeout: Request timeout in seconds
        """
        self._client = AsyncClient(
            token=token,
            api_url=api_url,
            api_version=api_version,
            timeout=timeout,
        )

        # Initialize API modules
        self.bots = AsyncBots(self._client)
        self.chats = AsyncChats(self._client)
        self.messages = AsyncMessages(self._client)
        self.subscriptions = AsyncSubscriptions(self._client)
        self.uploads = AsyncUploads(self._client)

        # Internal state
        self._marker: int | None = None
        self._running = False

    async def close(self) -> None:
        """Close the bot client."""
        await self._client.close()

    async def __aenter__(self) -> "AsyncMaxBot":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def get_updates(
        self,
        limit: int = 50,
        timeout: int = 30,
        marker: int | None = None,
        types: list[str] | None = None,
    ) -> UpdateList:
        """Get updates (long polling).

        Args:
            limit: Maximum number of updates to receive
            timeout: Long polling timeout in seconds
            marker: Update marker for pagination
            types: Types of updates to receive

        Returns:
            List of updates
        """
        params = {
            "limit": min(limit, 50),
            "timeout": timeout,
        }
        if marker is not None:
            params["marker"] = marker
        if types:
            params["types"] = ",".join(types)

        return await self._client.request_model("GET", "updates", UpdateList, params=params)

    async def poll_updates(
        self,
        limit: int = 50,
        timeout: int = 30,
        types: list[str] | None = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> AsyncIterator[UpdateType]:
        """Poll for updates continuously.

        Args:
            limit: Maximum number of updates per request
            timeout: Long polling timeout in seconds
            types: Types of updates to receive
            max_retries: Maximum retry attempts on error
            retry_delay: Initial delay between retries

        Yields:
            Update objects
        """
        self._running = True
        retry_count = 0

        while self._running:
            try:
                updates = await self.get_updates(
                    limit=limit,
                    timeout=timeout,
                    marker=self._marker,
                    types=types,
                )

                retry_count = 0

                if updates.marker is not None:
                    self._marker = updates.marker

                for update in updates.updates:
                    if not self._running:
                        break
                    yield update

            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error(f"Max retries reached, stopping: {e}")
                    self._running = False
                    raise

                delay = retry_delay * (2 ** (retry_count - 1))
                logger.warning(f"Error polling updates, retrying in {delay}s: {e}")
                await asyncio.sleep(delay)

    def stop_polling(self) -> None:
        """Stop the polling loop."""
        self._running = False

    def handle_webhook(self, data: dict) -> UpdateType:
        """Handle incoming webhook data.

        Args:
            data: Raw webhook data

        Returns:
            Parsed update object
        """
        return _parse_update(data)
