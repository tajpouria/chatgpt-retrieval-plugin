from typing import Dict, Any

from pydantic import BaseModel

from bot.schemas.common import Account


class Contact(BaseModel):
    id: int
    name: str
    account: Dict[str, Any]
    additional_attributes: Dict[str, Any]
    avatar: str
    custom_attributes: Dict[str, Any]
    email: str
    identifier: str
    phone_number: str
    thumbnail: str


class Inbox(BaseModel):
    id: int
    name: str


class Browser(BaseModel):
    browser_name: str
    browser_version: str
    device_name: str
    platform_name: str
    platform_version: str


class EventInfo(BaseModel):
    initiated_at: Dict[str, str]
    referer: str
    widget_language: str
    browser_language: str
    browser: Browser


class WebWidgetTriggeredEvent(BaseModel):
    id: int
    contact: Contact
    inbox: Inbox
    account: Account
    current_conversation: Any
    source_id: str
    event: str
    event_info: EventInfo
