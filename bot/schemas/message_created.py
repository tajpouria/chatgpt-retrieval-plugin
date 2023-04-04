from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

from bot.schemas.common import Account


class ContentType(str, Enum):
    text = "text"


class ContactInbox(BaseModel):
    id: int
    contact_id: int
    inbox_id: int
    source_id: str
    created_at: str
    updated_at: str
    hmac_verified: bool
    pubsub_token: str


class Message_type(str, Enum):
    incoming = "incoming"
    outgoing = "outgoing"


class MessageAuthor(BaseModel):
    id: int
    name: str
    email: Optional[str]
    additional_attributes: Dict[str, str]


class Conversation(BaseModel):
    assignee_id: Optional[int]
    unread_count: int


class Message(BaseModel):
    id: int
    content: str
    account_id: int
    inbox_id: int
    conversation_id: int
    message_type: Message_type
    created_at: int
    updated_at: str
    private: bool
    status: str
    source_id: Optional[str]
    content_type: str
    content_attributes: Dict[str, str]
    sender_type: str
    sender_id: int
    external_source_ids: Dict[str, str]
    additional_attributes: Dict[str, str]
    label_list: Optional[List[str]]
    conversation: Optional[Conversation]
    sender: MessageAuthor


class MessageCreatedEvent(BaseModel):
    account: Account
    additional_attributes: Dict[str, str]
    content_attributes: Dict[str, str]
    content_type: ContentType
    content: str
    conversation: Dict[str, Any]
    created_at: str
    id: int
    inbox: Dict[str, str]
    message_type: str
    private: bool
    sender: Dict[str, Any]
    source_id: Optional[str]
    event: str
    contact_inbox: ContactInbox
    messages: List[Message]
    labels: List[str]
    meta: Dict[str, Any]
    status: str
    custom_attributes: Dict[str, str]
    snoozed_until: Optional[str]
    unread_count: int
    first_reply_created_at: Optional[str]
    agent_last_seen_at: int
    contact_last_seen_at: int
    timestamp: int
