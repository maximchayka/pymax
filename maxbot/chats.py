"""Chat API methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

from maxbot.schemes import (
    ActionRequestBody,
    Chat,
    ChatAdminsResult,
    ChatList,
    ChatMember,
    ChatMembersResult,
    ChatPatch,
    SenderAction,
    SimpleQueryResult,
    UserIdsList,
)

if TYPE_CHECKING:
    from maxbot.client import AsyncClient, Client


class Chats:
    """Chat management API."""

    def __init__(self, client: "Client") -> None:
        self._client = client

    def get_chats(
        self,
        count: int | None = None,
        marker: int | None = None,
    ) -> ChatList:
        """Get chats the bot participated in.

        Args:
            count: Number of chats to return
            marker: Pagination marker

        Returns:
            List of chats with pagination marker
        """
        params = {}
        if count is not None:
            params["count"] = count
        if marker is not None:
            params["marker"] = marker

        return self._client.request_model("GET", "chats", ChatList, params=params)

    def get_chat(self, chat_id: int) -> Chat:
        """Get chat information by ID.

        Args:
            chat_id: Chat ID

        Returns:
            Chat information
        """
        return self._client.request_model("GET", f"chats/{chat_id}", Chat)

    def get_chat_membership(self, chat_id: int) -> ChatMember:
        """Get chat membership info for current bot.

        Args:
            chat_id: Chat ID

        Returns:
            Chat membership information
        """
        return self._client.request_model("GET", f"chats/{chat_id}/members/me", ChatMember)

    def get_chat_members(
        self,
        chat_id: int,
        count: int | None = None,
        marker: int | None = None,
        user_ids: list[int] | None = None,
    ) -> ChatMembersResult:
        """Get users in a chat.

        Args:
            chat_id: Chat ID
            count: Number of members to return
            marker: Pagination marker
            user_ids: Filter by specific user IDs

        Returns:
            List of chat members
        """
        params = {}
        if count is not None:
            params["count"] = count
        if marker is not None:
            params["marker"] = marker
        if user_ids:
            params["user_ids"] = ",".join(str(uid) for uid in user_ids)

        return self._client.request_model(
            "GET", f"chats/{chat_id}/members", ChatMembersResult, params=params
        )

    def get_specific_chat_members(
        self,
        chat_id: int,
        user_ids: list[int],
    ) -> ChatMembersResult:
        """Get info for specific users in a chat.

        Args:
            chat_id: Chat ID
            user_ids: List of user IDs

        Returns:
            Chat members information
        """
        body = UserIdsList(user_ids=user_ids)
        return self._client.request_model(
            "GET", f"chats/{chat_id}/members", ChatMembersResult, body=body
        )

    def get_chat_admins(self, chat_id: int) -> ChatAdminsResult:
        """Get chat administrators.

        Args:
            chat_id: Chat ID

        Returns:
            List of chat admins
        """
        return self._client.request_model("GET", f"chats/{chat_id}/members/admins", ChatAdminsResult)

    def leave_chat(self, chat_id: int) -> SimpleQueryResult:
        """Leave a chat (remove bot from members).

        Args:
            chat_id: Chat ID

        Returns:
            Operation result
        """
        return self._client.request_model("DELETE", f"chats/{chat_id}/members/me", SimpleQueryResult)

    def edit_chat(self, chat_id: int, patch: ChatPatch) -> Chat:
        """Edit chat properties.

        Args:
            chat_id: Chat ID
            patch: Chat patch data

        Returns:
            Updated chat information
        """
        return self._client.request_model("PATCH", f"chats/{chat_id}", Chat, body=patch)

    def add_member(self, chat_id: int, user_ids: list[int]) -> SimpleQueryResult:
        """Add members to a chat.

        Args:
            chat_id: Chat ID
            user_ids: List of user IDs to add

        Returns:
            Operation result
        """
        body = UserIdsList(user_ids=user_ids)
        return self._client.request_model(
            "POST", f"chats/{chat_id}/members", SimpleQueryResult, body=body
        )

    def remove_member(self, chat_id: int, user_id: int, block: bool = False) -> SimpleQueryResult:
        """Remove a member from a chat.

        Args:
            chat_id: Chat ID
            user_id: User ID to remove
            block: Whether to block the user

        Returns:
            Operation result
        """
        params = {"user_id": user_id}
        if block:
            params["block"] = "true"
        return self._client.request_model(
            "DELETE", f"chats/{chat_id}/members", SimpleQueryResult, params=params
        )

    def send_action(self, chat_id: int, action: SenderAction) -> SimpleQueryResult:
        """Send bot action to a chat (e.g., typing indicator).

        Args:
            chat_id: Chat ID
            action: Action to send

        Returns:
            Operation result
        """
        body = ActionRequestBody(action=action)
        return self._client.request_model(
            "POST", f"chats/{chat_id}/actions", SimpleQueryResult, body=body
        )


class AsyncChats:
    """Async chat management API."""

    def __init__(self, client: "AsyncClient") -> None:
        self._client = client

    async def get_chats(
        self,
        count: int | None = None,
        marker: int | None = None,
    ) -> ChatList:
        """Get chats the bot participated in."""
        params = {}
        if count is not None:
            params["count"] = count
        if marker is not None:
            params["marker"] = marker

        return await self._client.request_model("GET", "chats", ChatList, params=params)

    async def get_chat(self, chat_id: int) -> Chat:
        """Get chat information by ID."""
        return await self._client.request_model("GET", f"chats/{chat_id}", Chat)

    async def get_chat_membership(self, chat_id: int) -> ChatMember:
        """Get chat membership info for current bot."""
        return await self._client.request_model("GET", f"chats/{chat_id}/members/me", ChatMember)

    async def get_chat_members(
        self,
        chat_id: int,
        count: int | None = None,
        marker: int | None = None,
        user_ids: list[int] | None = None,
    ) -> ChatMembersResult:
        """Get users in a chat."""
        params = {}
        if count is not None:
            params["count"] = count
        if marker is not None:
            params["marker"] = marker
        if user_ids:
            params["user_ids"] = ",".join(str(uid) for uid in user_ids)

        return await self._client.request_model(
            "GET", f"chats/{chat_id}/members", ChatMembersResult, params=params
        )

    async def get_specific_chat_members(
        self,
        chat_id: int,
        user_ids: list[int],
    ) -> ChatMembersResult:
        """Get info for specific users in a chat."""
        body = UserIdsList(user_ids=user_ids)
        return await self._client.request_model(
            "GET", f"chats/{chat_id}/members", ChatMembersResult, body=body
        )

    async def get_chat_admins(self, chat_id: int) -> ChatAdminsResult:
        """Get chat administrators."""
        return await self._client.request_model(
            "GET", f"chats/{chat_id}/members/admins", ChatAdminsResult
        )

    async def leave_chat(self, chat_id: int) -> SimpleQueryResult:
        """Leave a chat."""
        return await self._client.request_model(
            "DELETE", f"chats/{chat_id}/members/me", SimpleQueryResult
        )

    async def edit_chat(self, chat_id: int, patch: ChatPatch) -> Chat:
        """Edit chat properties."""
        return await self._client.request_model("PATCH", f"chats/{chat_id}", Chat, body=patch)

    async def add_member(self, chat_id: int, user_ids: list[int]) -> SimpleQueryResult:
        """Add members to a chat."""
        body = UserIdsList(user_ids=user_ids)
        return await self._client.request_model(
            "POST", f"chats/{chat_id}/members", SimpleQueryResult, body=body
        )

    async def remove_member(
        self, chat_id: int, user_id: int, block: bool = False
    ) -> SimpleQueryResult:
        """Remove a member from a chat."""
        params = {"user_id": user_id}
        if block:
            params["block"] = "true"
        return await self._client.request_model(
            "DELETE", f"chats/{chat_id}/members", SimpleQueryResult, params=params
        )

    async def send_action(self, chat_id: int, action: SenderAction) -> SimpleQueryResult:
        """Send bot action to a chat."""
        body = ActionRequestBody(action=action)
        return await self._client.request_model(
            "POST", f"chats/{chat_id}/actions", SimpleQueryResult, body=body
        )
