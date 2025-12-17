"""Keyboard builder for Max Bot API."""

from __future__ import annotations

from maxbot.schemes import (
    Button,
    ButtonType,
    CallbackButton,
    ChatButton,
    InlineKeyboardAttachment,
    InlineKeyboardAttachmentPayload,
    LinkButton,
    OpenAppButton,
    RequestContactButton,
    RequestGeoLocationButton,
)


class KeyboardRow:
    """Keyboard row builder."""

    def __init__(self) -> None:
        self._buttons: list[ButtonType] = []

    def add_button(self, button: ButtonType) -> "KeyboardRow":
        """Add a custom button.

        Args:
            button: Button to add

        Returns:
            Self for chaining
        """
        self._buttons.append(button)
        return self

    def add_callback(
        self,
        text: str,
        payload: str,
        intent: str = "default",
    ) -> "KeyboardRow":
        """Add a callback button.

        Args:
            text: Button text
            payload: Callback payload
            intent: Button intent (default, positive, negative)

        Returns:
            Self for chaining
        """
        self._buttons.append(
            CallbackButton(text=text, payload=payload, intent=intent)
        )
        return self

    def add_link(self, text: str, url: str) -> "KeyboardRow":
        """Add a link button.

        Args:
            text: Button text
            url: Link URL

        Returns:
            Self for chaining
        """
        self._buttons.append(LinkButton(text=text, url=url))
        return self

    def add_contact(self, text: str = "Share Contact") -> "KeyboardRow":
        """Add a request contact button.

        Args:
            text: Button text

        Returns:
            Self for chaining
        """
        self._buttons.append(RequestContactButton(text=text))
        return self

    def add_geolocation(
        self,
        text: str = "Share Location",
        quick: bool = False,
    ) -> "KeyboardRow":
        """Add a request geolocation button.

        Args:
            text: Button text
            quick: Quick location mode

        Returns:
            Self for chaining
        """
        self._buttons.append(RequestGeoLocationButton(text=text, quick=quick))
        return self

    def add_chat(
        self,
        text: str,
        chat_title: str | None = None,
        chat_description: str | None = None,
        start_payload: str | None = None,
    ) -> "KeyboardRow":
        """Add a chat button.

        Args:
            text: Button text
            chat_title: Chat title
            chat_description: Chat description
            start_payload: Start payload

        Returns:
            Self for chaining
        """
        self._buttons.append(
            ChatButton(
                text=text,
                chat_title=chat_title,
                chat_description=chat_description,
                start_payload=start_payload,
            )
        )
        return self

    def add_open_app(
        self,
        text: str,
        url: str,
        app_id: str | None = None,
        chat: str | None = None,
        hash: str | None = None,
    ) -> "KeyboardRow":
        """Add an open app button.

        Args:
            text: Button text
            url: App URL
            app_id: App ID
            chat: Chat
            hash: Hash

        Returns:
            Self for chaining
        """
        self._buttons.append(
            OpenAppButton(
                text=text,
                url=url,
                app_id=app_id,
                chat=chat,
                hash=hash,
            )
        )
        return self

    def build(self) -> list[ButtonType]:
        """Build the row.

        Returns:
            List of buttons
        """
        return self._buttons


class KeyboardBuilder:
    """Keyboard builder."""

    def __init__(self) -> None:
        self._rows: list[list[ButtonType]] = []

    def add_row(self) -> KeyboardRow:
        """Add a new row and return row builder.

        Returns:
            Row builder for chaining
        """
        row = KeyboardRow()
        self._rows.append(row._buttons)
        return row

    def row(self, *buttons: ButtonType) -> "KeyboardBuilder":
        """Add a row with buttons.

        Args:
            *buttons: Buttons to add

        Returns:
            Self for chaining
        """
        self._rows.append(list(buttons))
        return self

    def callback(
        self,
        text: str,
        payload: str,
        intent: str = "default",
    ) -> "KeyboardBuilder":
        """Add a single callback button in a new row.

        Args:
            text: Button text
            payload: Callback payload
            intent: Button intent

        Returns:
            Self for chaining
        """
        self._rows.append([CallbackButton(text=text, payload=payload, intent=intent)])
        return self

    def link(self, text: str, url: str) -> "KeyboardBuilder":
        """Add a single link button in a new row.

        Args:
            text: Button text
            url: Link URL

        Returns:
            Self for chaining
        """
        self._rows.append([LinkButton(text=text, url=url)])
        return self

    def build(self) -> InlineKeyboardAttachment:
        """Build the keyboard attachment.

        Returns:
            Inline keyboard attachment
        """
        return InlineKeyboardAttachment(
            payload=InlineKeyboardAttachmentPayload(buttons=self._rows)
        )

    def to_dict(self) -> dict:
        """Convert to dictionary.

        Returns:
            Keyboard as dictionary
        """
        return self.build().model_dump(by_alias=True, exclude_none=True)
