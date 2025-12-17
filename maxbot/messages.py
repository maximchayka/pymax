"""Message API methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

from maxbot.keyboard import KeyboardBuilder
from maxbot.schemes import (
    Message,
    MessageCallbackResult,
    MessageList,
    NewMessageBody,
    SendMessageResult,
    SimpleQueryResult,
)

if TYPE_CHECKING:
    from maxbot.client import AsyncClient, Client


class Messages:
    """Message management API."""

    def __init__(self, client: "Client") -> None:
        self._client = client

    def get_messages(
        self,
        chat_id: int | None = None,
        message_ids: list[str] | None = None,
        from_time: int | None = None,
        to_time: int | None = None,
        count: int | None = None,
    ) -> MessageList:
        """Get messages from a chat.

        Args:
            chat_id: Chat ID to get messages from
            message_ids: Specific message IDs to retrieve
            from_time: Start timestamp
            to_time: End timestamp
            count: Number of messages to return

        Returns:
            List of messages
        """
        params = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        if message_ids:
            params["message_ids"] = ",".join(message_ids)
        if from_time is not None:
            params["from"] = from_time
        if to_time is not None:
            params["to"] = to_time
        if count is not None:
            params["count"] = count

        return self._client.request_model("GET", "messages", MessageList, params=params)

    def get_message(self, message_id: str) -> Message:
        """Get a specific message by ID.

        Args:
            message_id: Message ID

        Returns:
            Message data
        """
        return self._client.request_model("GET", f"messages/{message_id}", Message)

    def send(
        self,
        chat_id: int | None = None,
        user_id: int | None = None,
        text: str | None = None,
        keyboard: KeyboardBuilder | None = None,
        attachments: list | None = None,
        link: dict | None = None,
        notify: bool = True,
        format: str | None = None,
        disable_link_preview: bool = False,
    ) -> SendMessageResult:
        """Send a message.

        Args:
            chat_id: Chat ID to send to
            user_id: User ID to send to (for direct messages)
            text: Message text
            keyboard: Keyboard builder with buttons
            attachments: List of attachments
            link: Reply/forward link
            notify: Whether to send notification
            format: Text format (html, markdown)
            disable_link_preview: Disable URL preview

        Returns:
            Send result with message data
        """
        params = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        if user_id is not None:
            params["user_id"] = user_id
        if disable_link_preview:
            params["disable_link_preview"] = "true"

        # Build attachments list
        attach_list = list(attachments) if attachments else []

        # Add keyboard if provided
        if keyboard is not None:
            attach_list.append(keyboard.build())

        body = NewMessageBody(
            text=text,
            attachments=attach_list if attach_list else None,
            link=link,
            notify=notify,
            format=format,
        )

        return self._client.request_model(
            "POST", "messages", SendMessageResult, params=params, body=body
        )

    def edit_message(
        self,
        message_id: str,
        text: str | None = None,
        keyboard: KeyboardBuilder | None = None,
        attachments: list | None = None,
        link: dict | None = None,
        notify: bool = True,
        format: str | None = None,
    ) -> SendMessageResult:
        """Edit a message.

        Args:
            message_id: Message ID to edit
            text: New message text
            keyboard: New keyboard
            attachments: New attachments
            link: New link
            notify: Whether to notify
            format: Text format

        Returns:
            Updated message data
        """
        attach_list = list(attachments) if attachments else []
        if keyboard is not None:
            attach_list.append(keyboard.build())

        body = NewMessageBody(
            text=text,
            attachments=attach_list if attach_list else None,
            link=link,
            notify=notify,
            format=format,
        )

        return self._client.request_model(
            "PUT", f"messages/{message_id}", SendMessageResult, body=body
        )

    def delete_message(self, message_id: str) -> SimpleQueryResult:
        """Delete a message.

        Args:
            message_id: Message ID to delete

        Returns:
            Operation result
        """
        return self._client.request_model("DELETE", f"messages/{message_id}", SimpleQueryResult)

    def answer_on_callback(
        self,
        callback_id: str,
        message: str | None = None,
        notification: bool = False,
    ) -> MessageCallbackResult:
        """Answer a callback query (button click).

        Args:
            callback_id: Callback query ID
            message: Response message
            notification: Whether to show as notification

        Returns:
            Callback result
        """
        body = {
            "callback_id": callback_id,
        }
        if message is not None:
            body["message"] = message
        if notification:
            body["notification"] = notification

        return self._client.request_model(
            "POST", "answers", MessageCallbackResult, body=body
        )

    def check(self, phones: list[str]) -> dict:
        """Check if phone numbers are registered in Max.

        Args:
            phones: List of phone numbers

        Returns:
            Check result
        """
        params = {"phones": ",".join(phones)}
        return self._client.request("GET", "users/check", params=params)

    def list_exist(self, phones: list[str]) -> dict:
        """Get list of existing users by phone numbers.

        Args:
            phones: List of phone numbers

        Returns:
            List of existing users
        """
        body = {"phones": phones}
        return self._client.request("POST", "users/check", body=body)


class AsyncMessages:
    """Async message management API."""

    def __init__(self, client: "AsyncClient") -> None:
        self._client = client

    async def get_messages(
        self,
        chat_id: int | None = None,
        message_ids: list[str] | None = None,
        from_time: int | None = None,
        to_time: int | None = None,
        count: int | None = None,
    ) -> MessageList:
        """Get messages from a chat."""
        params = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        if message_ids:
            params["message_ids"] = ",".join(message_ids)
        if from_time is not None:
            params["from"] = from_time
        if to_time is not None:
            params["to"] = to_time
        if count is not None:
            params["count"] = count

        return await self._client.request_model("GET", "messages", MessageList, params=params)

    async def get_message(self, message_id: str) -> Message:
        """Get a specific message by ID."""
        return await self._client.request_model("GET", f"messages/{message_id}", Message)

    async def send(
        self,
        chat_id: int | None = None,
        user_id: int | None = None,
        text: str | None = None,
        keyboard: KeyboardBuilder | None = None,
        attachments: list | None = None,
        link: dict | None = None,
        notify: bool = True,
        format: str | None = None,
        disable_link_preview: bool = False,
    ) -> SendMessageResult:
        """Send a message."""
        params = {}
        if chat_id is not None:
            params["chat_id"] = chat_id
        if user_id is not None:
            params["user_id"] = user_id
        if disable_link_preview:
            params["disable_link_preview"] = "true"

        attach_list = list(attachments) if attachments else []
        if keyboard is not None:
            attach_list.append(keyboard.build())

        body = NewMessageBody(
            text=text,
            attachments=attach_list if attach_list else None,
            link=link,
            notify=notify,
            format=format,
        )

        return await self._client.request_model(
            "POST", "messages", SendMessageResult, params=params, body=body
        )

    async def edit_message(
        self,
        message_id: str,
        text: str | None = None,
        keyboard: KeyboardBuilder | None = None,
        attachments: list | None = None,
        link: dict | None = None,
        notify: bool = True,
        format: str | None = None,
    ) -> SendMessageResult:
        """Edit a message."""
        attach_list = list(attachments) if attachments else []
        if keyboard is not None:
            attach_list.append(keyboard.build())

        body = NewMessageBody(
            text=text,
            attachments=attach_list if attach_list else None,
            link=link,
            notify=notify,
            format=format,
        )

        return await self._client.request_model(
            "PUT", f"messages/{message_id}", SendMessageResult, body=body
        )

    async def delete_message(self, message_id: str) -> SimpleQueryResult:
        """Delete a message."""
        return await self._client.request_model(
            "DELETE", f"messages/{message_id}", SimpleQueryResult
        )

    async def answer_on_callback(
        self,
        callback_id: str,
        message: str | None = None,
        notification: bool = False,
    ) -> MessageCallbackResult:
        """Answer a callback query."""
        body = {
            "callback_id": callback_id,
        }
        if message is not None:
            body["message"] = message
        if notification:
            body["notification"] = notification

        return await self._client.request_model(
            "POST", "answers", MessageCallbackResult, body=body
        )

    async def check(self, phones: list[str]) -> dict:
        """Check if phone numbers are registered."""
        params = {"phones": ",".join(phones)}
        return await self._client.request("GET", "users/check", params=params)

    async def list_exist(self, phones: list[str]) -> dict:
        """Get list of existing users by phone numbers."""
        body = {"phones": phones}
        return await self._client.request("POST", "users/check", body=body)
