"""Pydantic models for Max Bot API."""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Enums
# ============================================================================


class ChatType(str, Enum):
    """Chat type enumeration."""

    DIALOG = "dialog"
    CHAT = "chat"
    CHANNEL = "channel"


class ChatStatus(str, Enum):
    """Chat status enumeration."""

    ACTIVE = "active"
    REMOVED = "removed"
    LEFT = "left"
    CLOSED = "closed"
    SUSPENDED = "suspended"


class SenderAction(str, Enum):
    """Sender action enumeration."""

    TYPING_ON = "typing_on"
    SENDING_PHOTO = "sending_photo"
    SENDING_VIDEO = "sending_video"
    SENDING_AUDIO = "sending_audio"
    SENDING_FILE = "sending_file"
    MARK_SEEN = "mark_seen"


class UploadType(str, Enum):
    """Upload type enumeration."""

    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"


# ============================================================================
# Base Models
# ============================================================================


class MaxBotModel(BaseModel):
    """Base model with common configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="allow",
    )


# ============================================================================
# User Models
# ============================================================================


class User(MaxBotModel):
    """User information."""

    user_id: int = Field(alias="user_id")
    name: str
    username: str | None = None
    is_bot: bool = Field(default=False, alias="is_bot")
    last_activity_time: int = Field(default=0, alias="last_activity_time")


class UserWithPhoto(User):
    """User with photo information."""

    avatar_url: str | None = Field(default=None, alias="avatar_url")
    full_avatar_url: str | None = Field(default=None, alias="full_avatar_url")


class UserIdsList(MaxBotModel):
    """List of user IDs."""

    user_ids: list[int] = Field(default_factory=list, alias="user_ids")


# ============================================================================
# Bot Models
# ============================================================================


class BotCommand(MaxBotModel):
    """Bot command."""

    name: str
    description: str | None = None


class BotInfo(MaxBotModel):
    """Bot information."""

    user_id: int = Field(alias="user_id")
    name: str
    username: str | None = None
    avatar_url: str | None = Field(default=None, alias="avatar_url")
    full_avatar_url: str | None = Field(default=None, alias="full_avatar_url")
    commands: list[BotCommand] | None = None
    description: str | None = None


class BotPatch(MaxBotModel):
    """Bot patch request body."""

    name: str | None = None
    username: str | None = None
    description: str | None = None
    commands: list[BotCommand] | None = None
    photo: PhotoAttachmentRequest | None = None


# ============================================================================
# Chat Models
# ============================================================================


class Chat(MaxBotModel):
    """Chat information."""

    chat_id: int = Field(alias="chat_id")
    type: ChatType
    status: ChatStatus
    title: str | None = None
    icon: PhotoAttachmentPayload | None = None
    last_event_time: int = Field(default=0, alias="last_event_time")
    participants_count: int = Field(default=0, alias="participants_count")
    owner_id: int | None = Field(default=None, alias="owner_id")
    participants: dict[str, int] | None = None
    is_public: bool = Field(default=False, alias="is_public")
    link: str | None = None
    description: str | None = None
    dialog_with_user: UserWithPhoto | None = Field(default=None, alias="dialog_with_user")
    messages_count: int | None = Field(default=None, alias="messages_count")
    chat_message_id: str | None = Field(default=None, alias="chat_message_id")
    pinned_message: Message | None = Field(default=None, alias="pinned_message")


class ChatList(MaxBotModel):
    """List of chats."""

    chats: list[Chat] = Field(default_factory=list)
    marker: int | None = None


class ChatMember(MaxBotModel):
    """Chat member information."""

    user_id: int = Field(alias="user_id")
    name: str
    username: str | None = None
    avatar_url: str | None = Field(default=None, alias="avatar_url")
    full_avatar_url: str | None = Field(default=None, alias="full_avatar_url")
    last_access_time: int = Field(default=0, alias="last_access_time")
    is_owner: bool = Field(default=False, alias="is_owner")
    is_admin: bool = Field(default=False, alias="is_admin")
    join_time: int = Field(default=0, alias="join_time")
    is_bot: bool = Field(default=False, alias="is_bot")
    permissions: list[str] | None = None
    last_activity_time: int = Field(default=0, alias="last_activity_time")
    description: str | None = None


class ChatMembersResult(MaxBotModel):
    """Chat members result."""

    members: list[ChatMember] = Field(default_factory=list)
    marker: int | None = None


class ChatAdminsResult(MaxBotModel):
    """Chat admins result."""

    admins: list[ChatMember] = Field(default_factory=list, alias="members")


class ChatPatch(MaxBotModel):
    """Chat patch request body."""

    title: str | None = None
    icon: PhotoAttachmentRequest | None = None
    pin: str | None = None
    notify: bool | None = None


# ============================================================================
# Button Models
# ============================================================================


class Button(MaxBotModel):
    """Base button."""

    type: str
    text: str


class CallbackButton(Button):
    """Callback button."""

    type: Literal["callback"] = "callback"
    payload: str
    intent: str = "default"


class LinkButton(Button):
    """Link button."""

    type: Literal["link"] = "link"
    url: str


class RequestContactButton(Button):
    """Request contact button."""

    type: Literal["request_contact"] = "request_contact"


class RequestGeoLocationButton(Button):
    """Request geolocation button."""

    type: Literal["request_geo_location"] = "request_geo_location"
    quick: bool = False


class ChatButton(Button):
    """Chat button."""

    type: Literal["chat"] = "chat"
    chat_title: str | None = Field(default=None, alias="chat_title")
    chat_description: str | None = Field(default=None, alias="chat_description")
    start_payload: str | None = Field(default=None, alias="start_payload")
    uuid: str | None = None


class OpenAppButton(Button):
    """Open app button."""

    type: Literal["open_app"] = "open_app"
    url: str
    app_id: str | None = Field(default=None, alias="app_id")
    chat: str | None = None
    hash: str | None = None


ButtonType = Union[
    CallbackButton,
    LinkButton,
    RequestContactButton,
    RequestGeoLocationButton,
    ChatButton,
    OpenAppButton,
    Button,
]


# ============================================================================
# Keyboard Model
# ============================================================================


class Keyboard(MaxBotModel):
    """Keyboard - 2D array of buttons."""

    buttons: list[list[ButtonType]] = Field(default_factory=list)


# ============================================================================
# Attachment Models
# ============================================================================


class AttachmentPayload(MaxBotModel):
    """Base attachment payload."""

    pass


class MediaAttachmentPayload(AttachmentPayload):
    """Media attachment payload."""

    token: str | None = None


class PhotoAttachmentPayload(MediaAttachmentPayload):
    """Photo attachment payload."""

    url: str | None = None
    token: str | None = None


class PhotoToken(MaxBotModel):
    """Photo token."""

    token: str


class VideoAttachmentPayload(MediaAttachmentPayload):
    """Video attachment payload."""

    url: str | None = None
    thumbnail: PhotoAttachmentPayload | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None


class AudioAttachmentPayload(MediaAttachmentPayload):
    """Audio attachment payload."""

    url: str | None = None


class FileAttachmentPayload(MediaAttachmentPayload):
    """File attachment payload."""

    url: str | None = None
    filename: str | None = None
    size: int | None = None


class StickerAttachmentPayload(AttachmentPayload):
    """Sticker attachment payload."""

    code: str
    url: str | None = None
    width: int | None = None
    height: int | None = None


class ContactAttachmentPayload(AttachmentPayload):
    """Contact attachment payload."""

    vcf_info: str | None = Field(default=None, alias="vcfInfo")
    max_info: UserWithPhoto | None = Field(default=None, alias="maxInfo")


class InlineKeyboardAttachmentPayload(AttachmentPayload):
    """Inline keyboard attachment payload."""

    buttons: list[list[ButtonType]] = Field(default_factory=list)


class LocationAttachmentPayload(AttachmentPayload):
    """Location attachment payload."""

    latitude: float
    longitude: float


class ShareAttachmentPayload(AttachmentPayload):
    """Share attachment payload."""

    url: str | None = None
    token: str | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = Field(default=None, alias="image_url")


# ============================================================================
# Attachment Request Models
# ============================================================================


class AttachmentRequest(MaxBotModel):
    """Base attachment request."""

    type: str


class PhotoAttachmentRequest(AttachmentRequest):
    """Photo attachment request."""

    type: Literal["image"] = "image"
    payload: PhotoAttachmentPayload


class VideoAttachmentRequest(AttachmentRequest):
    """Video attachment request."""

    type: Literal["video"] = "video"
    payload: VideoAttachmentPayload


class AudioAttachmentRequest(AttachmentRequest):
    """Audio attachment request."""

    type: Literal["audio"] = "audio"
    payload: AudioAttachmentPayload


class FileAttachmentRequest(AttachmentRequest):
    """File attachment request."""

    type: Literal["file"] = "file"
    payload: FileAttachmentPayload


class LocationAttachmentRequest(AttachmentRequest):
    """Location attachment request."""

    type: Literal["location"] = "location"
    payload: LocationAttachmentPayload


class ContactAttachmentRequest(AttachmentRequest):
    """Contact attachment request."""

    type: Literal["contact"] = "contact"
    payload: ContactAttachmentPayload


# ============================================================================
# Attachment Response Models
# ============================================================================


class Attachment(MaxBotModel):
    """Base attachment."""

    type: str


class PhotoAttachment(Attachment):
    """Photo attachment."""

    type: Literal["image"] = "image"
    payload: PhotoAttachmentPayload


class VideoAttachment(Attachment):
    """Video attachment."""

    type: Literal["video"] = "video"
    payload: VideoAttachmentPayload


class AudioAttachment(Attachment):
    """Audio attachment."""

    type: Literal["audio"] = "audio"
    payload: AudioAttachmentPayload


class FileAttachment(Attachment):
    """File attachment."""

    type: Literal["file"] = "file"
    payload: FileAttachmentPayload


class StickerAttachment(Attachment):
    """Sticker attachment."""

    type: Literal["sticker"] = "sticker"
    payload: StickerAttachmentPayload


class ContactAttachment(Attachment):
    """Contact attachment."""

    type: Literal["contact"] = "contact"
    payload: ContactAttachmentPayload


class InlineKeyboardAttachment(Attachment):
    """Inline keyboard attachment."""

    type: Literal["inline_keyboard"] = "inline_keyboard"
    payload: InlineKeyboardAttachmentPayload


class LocationAttachment(Attachment):
    """Location attachment."""

    type: Literal["location"] = "location"
    payload: LocationAttachmentPayload


class ShareAttachment(Attachment):
    """Share attachment."""

    type: Literal["share"] = "share"
    payload: ShareAttachmentPayload


AttachmentType = Union[
    PhotoAttachment,
    VideoAttachment,
    AudioAttachment,
    FileAttachment,
    StickerAttachment,
    ContactAttachment,
    InlineKeyboardAttachment,
    LocationAttachment,
    ShareAttachment,
    Attachment,
]


# ============================================================================
# Message Models
# ============================================================================


class MessageStat(MaxBotModel):
    """Message statistics."""

    views: int = 0


class NewMessageLink(MaxBotModel):
    """New message link."""

    type: str = "forward"
    mid: str = Field(alias="mid")
    chat_id: int | None = Field(default=None, alias="chat_id")


class MessageBody(MaxBotModel):
    """Message body."""

    mid: str = Field(alias="mid")
    seq: int = 0
    text: str | None = None
    attachments: list[AttachmentType] | None = None
    markup: str | None = None


class LinkedMessage(MaxBotModel):
    """Linked message (forwarded/replied)."""

    type: str = "forward"
    sender: UserWithPhoto | None = None
    chat_id: int | None = Field(default=None, alias="chat_id")
    message: MessageBody | None = None


class Recipient(MaxBotModel):
    """Message recipient."""

    chat_id: int | None = Field(default=None, alias="chat_id")
    chat_type: ChatType | None = Field(default=None, alias="chat_type")
    user_id: int | None = Field(default=None, alias="user_id")


class Message(MaxBotModel):
    """Full message."""

    sender: UserWithPhoto | None = None
    recipient: Recipient | None = None
    timestamp: int = 0
    link: LinkedMessage | None = None
    body: MessageBody
    stat: MessageStat | None = None
    url: str | None = None
    constructor: User | None = None


class MessageList(MaxBotModel):
    """List of messages."""

    messages: list[Message] = Field(default_factory=list)


class NewMessageBody(MaxBotModel):
    """New message body for sending."""

    text: str | None = None
    attachments: list[AttachmentRequest] | None = None
    link: NewMessageLink | None = None
    notify: bool = True
    format: str | None = None


class SendMessageResult(MaxBotModel):
    """Send message result."""

    message: Message


class MessageCallbackResult(MaxBotModel):
    """Message callback result."""

    success: bool = True
    message: str | None = None


# ============================================================================
# Subscription Models
# ============================================================================


class Subscription(MaxBotModel):
    """Webhook subscription."""

    url: str
    time: int = 0
    update_types: list[str] | None = Field(default=None, alias="update_types")
    version: str | None = None


class SubscriptionRequestBody(MaxBotModel):
    """Subscription request body."""

    url: str
    update_types: list[str] | None = Field(default=None, alias="update_types")
    version: str | None = None
    secret: str | None = None


class GetSubscriptionsResult(MaxBotModel):
    """Get subscriptions result."""

    subscriptions: list[Subscription] = Field(default_factory=list)


class SimpleQueryResult(MaxBotModel):
    """Simple query result."""

    success: bool = True
    message: str | None = None


# ============================================================================
# Update Models
# ============================================================================


class Update(MaxBotModel):
    """Base update."""

    update_type: str = Field(alias="update_type")
    timestamp: int = 0
    user_locale: str | None = Field(default=None, alias="user_locale")


class Callback(MaxBotModel):
    """Callback data."""

    timestamp: int = 0
    callback_id: str = Field(alias="callback_id")
    payload: str | None = None
    user: UserWithPhoto | None = None


class MessageCreatedUpdate(Update):
    """Message created update."""

    update_type: Literal["message_created"] = Field(default="message_created", alias="update_type")
    message: Message


class MessageEditedUpdate(Update):
    """Message edited update."""

    update_type: Literal["message_edited"] = Field(default="message_edited", alias="update_type")
    message: Message


class MessageRemovedUpdate(Update):
    """Message removed update."""

    update_type: Literal["message_removed"] = Field(default="message_removed", alias="update_type")
    message_id: str = Field(alias="message_id")
    chat_id: int = Field(alias="chat_id")
    user_id: int = Field(alias="user_id")


class MessageCallbackUpdate(Update):
    """Message callback update."""

    update_type: Literal["message_callback"] = Field(
        default="message_callback", alias="update_type"
    )
    callback: Callback
    message: Message | None = None
    user_locale: str | None = Field(default=None, alias="user_locale")


class MessageChatCreatedUpdate(Update):
    """Message chat created update."""

    update_type: Literal["message_chat_created"] = Field(
        default="message_chat_created", alias="update_type"
    )
    chat: Chat
    message_id: str | None = Field(default=None, alias="message_id")
    start_payload: str | None = Field(default=None, alias="start_payload")


class MessageConstructionRequest(MaxBotModel):
    """Message construction request."""

    session_id: str = Field(alias="session_id")
    user: UserWithPhoto
    user_locale: str | None = Field(default=None, alias="user_locale")
    data: str | None = None
    input: str | None = None


class MessageConstructedUpdate(Update):
    """Message constructed update."""

    update_type: Literal["message_constructed"] = Field(
        default="message_constructed", alias="update_type"
    )
    session_id: str = Field(alias="session_id")
    message: Message | None = None


class BotAddedToChatUpdate(Update):
    """Bot added to chat update."""

    update_type: Literal["bot_added"] = Field(default="bot_added", alias="update_type")
    chat_id: int = Field(alias="chat_id")
    user: UserWithPhoto
    is_channel: bool = Field(default=False, alias="is_channel")


class BotRemovedFromChatUpdate(Update):
    """Bot removed from chat update."""

    update_type: Literal["bot_removed"] = Field(default="bot_removed", alias="update_type")
    chat_id: int = Field(alias="chat_id")
    user: UserWithPhoto
    is_channel: bool = Field(default=False, alias="is_channel")


class BotStartedUpdate(Update):
    """Bot started update."""

    update_type: Literal["bot_started"] = Field(default="bot_started", alias="update_type")
    chat_id: int = Field(alias="chat_id")
    user: UserWithPhoto
    payload: str | None = None


class UserAddedToChatUpdate(Update):
    """User added to chat update."""

    update_type: Literal["user_added"] = Field(default="user_added", alias="update_type")
    chat_id: int = Field(alias="chat_id")
    user: UserWithPhoto
    inviter_id: int | None = Field(default=None, alias="inviter_id")
    is_channel: bool = Field(default=False, alias="is_channel")


class UserRemovedFromChatUpdate(Update):
    """User removed from chat update."""

    update_type: Literal["user_removed"] = Field(default="user_removed", alias="update_type")
    chat_id: int = Field(alias="chat_id")
    user: UserWithPhoto
    admin_id: int | None = Field(default=None, alias="admin_id")
    is_channel: bool = Field(default=False, alias="is_channel")


class ChatTitleChangedUpdate(Update):
    """Chat title changed update."""

    update_type: Literal["chat_title_changed"] = Field(
        default="chat_title_changed", alias="update_type"
    )
    chat_id: int = Field(alias="chat_id")
    user: UserWithPhoto
    title: str


UpdateType = Union[
    MessageCreatedUpdate,
    MessageEditedUpdate,
    MessageRemovedUpdate,
    MessageCallbackUpdate,
    MessageChatCreatedUpdate,
    MessageConstructedUpdate,
    BotAddedToChatUpdate,
    BotRemovedFromChatUpdate,
    BotStartedUpdate,
    UserAddedToChatUpdate,
    UserRemovedFromChatUpdate,
    ChatTitleChangedUpdate,
    Update,
]


class UpdateList(MaxBotModel):
    """List of updates."""

    updates: list[UpdateType] = Field(default_factory=list)
    marker: int | None = None


# ============================================================================
# Upload Models
# ============================================================================


class UploadEndpoint(MaxBotModel):
    """Upload endpoint."""

    url: str


class UploadedInfo(MaxBotModel):
    """Uploaded file info."""

    token: str | None = None
    url: str | None = None
    filename: str | None = None


# ============================================================================
# Action Models
# ============================================================================


class ActionRequestBody(MaxBotModel):
    """Action request body."""

    action: SenderAction


# Update forward references
Chat.model_rebuild()
