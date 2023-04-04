import os
from chatwoot.services.send_message_to_conversation import (
    send_message_to_conversation,
)
from chatwoot.schemas.common import AccountSettings
from bot.schemas.message_created import ContentType, MessageCreatedEvent
from services.logger import logger
from dict_deep import deep_get

CHATWOOT_URL = os.getenv("CHATWOOT_URL")
CHATWOOT_BOT_TOKEN = os.getenv("CHATWOOT_BOT_TOKEN")
CHATWOOT_PLATFORM_TOKEN = os.getenv("CHATWOOT_PLATFORM_TOKEN")
CHATWOOT_USER_TOKEN = os.getenv("CHATWOOT_USER_TOKEN")
CHATWOOT_AGENTBOT_OUTGOING_URL = os.getenv("CHATWOOT_AGENTBOT_OUTGOING_URL")


def process_message_created_event(event_data: MessageCreatedEvent):
    """Handle a 'message_created' event.

    Args:
        event_data: The event data, represented as a Pydantic model instance.

    Returns:
        None.
    """
    logger.info("Received a 'message_created' event: %s", event_data)

    message_type = event_data.get("message_type")
    if message_type == "outgoing":
        logger.info("Ignoring outgoing message")
        return

    content_type = ContentType(event_data.get("content_type"))
    if content_type == ContentType.text:
        handle_text_content(event_data)
        pass
    else:
        handle_unknown_content_type(event_data)
        pass


def handle_text_content(event_data: MessageCreatedEvent):
    """Handle text content.

    Args:
        event_data: The event data, represented as a Pydantic model instance.

    Returns:
        None.
    """

    logger.info(
        "Received a 'message_created' event with text content: %s",
        event_data.get("content"),
    )

    content = deep_get(event_data, "content")
    account_id = deep_get(event_data, "account.id")
    conversation_id = deep_get(event_data, "conversation.id")

    if not content or not account_id or not conversation_id:
        logger.error(
            "Received a 'message_created' event with missing content or account or conversation ID"
        )
        return

    # TODO: Must be calculated dynamically
    settings = AccountSettings(
        chatwoot_url=CHATWOOT_URL,
        chatwoot_bot_token=CHATWOOT_BOT_TOKEN,
        chatwoot_platform_token=CHATWOOT_PLATFORM_TOKEN,
        chatwoot_user_token=CHATWOOT_USER_TOKEN,
        chatwoot_account_id=account_id,
    )

    response = send_message_to_conversation(
        conversation_id,
        content,
        settings=settings,
    )
    status_code = response.status_code
    logger.info(
        "Send message to conversation response status: %s", response.status_code
    )
    if status_code != 200:
        logger.error("Send message to conversation response body: %s", response.text)


def handle_unknown_content_type(event_data: MessageCreatedEvent):
    """Handle unknown content types.

    Args:
        event_data: The event data, represented as a Pydantic model instance.

    Returns:
        None.
    """
    logger.warning(
        "Received a 'message_created' event with unknown content type: %s",
        event_data.get("content_type"),
    )
    pass
