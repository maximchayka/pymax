"""Max Bot API client for Python.

A Python library for Max Messenger Bot API.
"""

from maxbot.api import AsyncMaxBot, MaxBot
from maxbot.client import AsyncClient, Client
from maxbot.errors import (
    APIError,
    EmptyTokenError,
    InvalidURLError,
    MaxBotError,
    NetworkError,
    SerializationError,
    TimeoutError,
)
from maxbot.keyboard import KeyboardBuilder, KeyboardRow
from maxbot.schemes import (
    # Attachments
    Attachment,
    AttachmentRequest,
    AudioAttachment,
    AudioAttachmentRequest,
    ContactAttachment,
    ContactAttachmentRequest,
    FileAttachment,
    FileAttachmentRequest,
    InlineKeyboardAttachment,
    LocationAttachment,
    LocationAttachmentRequest,
    PhotoAttachment,
    PhotoAttachmentRequest,
    ShareAttachment,
    StickerAttachment,
    VideoAttachment,
    VideoAttachmentRequest,
    # Bot
    BotCommand,
    BotInfo,
    BotPatch,
    # Buttons
    Button,
    CallbackButton,
    ChatButton,
    LinkButton,
    OpenAppButton,
    RequestContactButton,
    RequestGeoLocationButton,
    # Chat
    Chat,
    ChatAdminsResult,
    ChatList,
    ChatMember,
    ChatMembersResult,
    ChatPatch,
    ChatStatus,
    ChatType,
    # Keyboard
    Keyboard,
    # Message
    LinkedMessage,
    Message,
    MessageBody,
    MessageCallbackResult,
    MessageList,
    MessageStat,
    NewMessageBody,
    NewMessageLink,
    SendMessageResult,
    # Recipient
    Recipient,
    # Subscription
    GetSubscriptionsResult,
    SimpleQueryResult,
    Subscription,
    SubscriptionRequestBody,
    # Updates
    BotAddedToChatUpdate,
    BotRemovedFromChatUpdate,
    BotStartedUpdate,
    Callback,
    ChatTitleChangedUpdate,
    MessageCallbackUpdate,
    MessageChatCreatedUpdate,
    MessageCreatedUpdate,
    MessageEditedUpdate,
    MessageConstructedUpdate,
    MessageConstructionRequest,
    MessageRemovedUpdate,
    Update,
    UpdateList,
    UserAddedToChatUpdate,
    UserRemovedFromChatUpdate,
    # Upload
    UploadEndpoint,
    UploadType,
    UploadedInfo,
    # User
    User,
    UserIdsList,
    UserWithPhoto,
    # Action
    ActionRequestBody,
    SenderAction,
)

__version__ = "1.0.0"

__all__ = [
    # Main classes
    "MaxBot",
    "AsyncMaxBot",
    "Client",
    "AsyncClient",
    "KeyboardBuilder",
    "KeyboardRow",
    # Errors
    "MaxBotError",
    "APIError",
    "EmptyTokenError",
    "InvalidURLError",
    "NetworkError",
    "SerializationError",
    "TimeoutError",
    # Attachments
    "Attachment",
    "AttachmentRequest",
    "AudioAttachment",
    "AudioAttachmentRequest",
    "ContactAttachment",
    "ContactAttachmentRequest",
    "FileAttachment",
    "FileAttachmentRequest",
    "InlineKeyboardAttachment",
    "LocationAttachment",
    "LocationAttachmentRequest",
    "PhotoAttachment",
    "PhotoAttachmentRequest",
    "ShareAttachment",
    "StickerAttachment",
    "VideoAttachment",
    "VideoAttachmentRequest",
    # Bot
    "BotCommand",
    "BotInfo",
    "BotPatch",
    # Buttons
    "Button",
    "CallbackButton",
    "ChatButton",
    "LinkButton",
    "OpenAppButton",
    "RequestContactButton",
    "RequestGeoLocationButton",
    # Chat
    "Chat",
    "ChatAdminsResult",
    "ChatList",
    "ChatMember",
    "ChatMembersResult",
    "ChatPatch",
    "ChatStatus",
    "ChatType",
    # Keyboard
    "Keyboard",
    # Message
    "LinkedMessage",
    "Message",
    "MessageBody",
    "MessageCallbackResult",
    "MessageList",
    "MessageStat",
    "NewMessageBody",
    "NewMessageLink",
    "SendMessageResult",
    # Recipient
    "Recipient",
    # Subscription
    "GetSubscriptionsResult",
    "SimpleQueryResult",
    "Subscription",
    "SubscriptionRequestBody",
    # Updates
    "BotAddedToChatUpdate",
    "BotRemovedFromChatUpdate",
    "BotStartedUpdate",
    "Callback",
    "ChatTitleChangedUpdate",
    "MessageCallbackUpdate",
    "MessageChatCreatedUpdate",
    "MessageCreatedUpdate",
    "MessageEditedUpdate",
    "MessageConstructedUpdate",
    "MessageConstructionRequest",
    "MessageRemovedUpdate",
    "Update",
    "UpdateList",
    "UserAddedToChatUpdate",
    "UserRemovedFromChatUpdate",
    # Upload
    "UploadEndpoint",
    "UploadType",
    "UploadedInfo",
    # User
    "User",
    "UserIdsList",
    "UserWithPhoto",
    # Action
    "ActionRequestBody",
    "SenderAction",
]
