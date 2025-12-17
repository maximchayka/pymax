"""Bot API methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

from maxbot.schemes import BotInfo, BotPatch

if TYPE_CHECKING:
    from maxbot.client import AsyncClient, Client


class Bots:
    """Bot management API."""

    def __init__(self, client: "Client") -> None:
        self._client = client

    def get_bot(self) -> BotInfo:
        """Get information about the current bot.

        Returns the bot's identifier, name, and avatar.
        Current bot is identified by the access token.

        Returns:
            Bot information
        """
        return self._client.request_model("GET", "me", BotInfo)

    def patch_bot(self, patch: BotPatch) -> BotInfo:
        """Edit current bot info.

        Fill only the fields you want to update.

        Args:
            patch: Bot patch data

        Returns:
            Updated bot information
        """
        return self._client.request_model("PATCH", "me", BotInfo, body=patch)


class AsyncBots:
    """Async bot management API."""

    def __init__(self, client: "AsyncClient") -> None:
        self._client = client

    async def get_bot(self) -> BotInfo:
        """Get information about the current bot.

        Returns:
            Bot information
        """
        return await self._client.request_model("GET", "me", BotInfo)

    async def patch_bot(self, patch: BotPatch) -> BotInfo:
        """Edit current bot info.

        Args:
            patch: Bot patch data

        Returns:
            Updated bot information
        """
        return await self._client.request_model("PATCH", "me", BotInfo, body=patch)
