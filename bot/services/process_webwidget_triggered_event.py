from bot.schemas.message_created import MessageCreatedEvent
from services.logger import logger


def process_webwidget_triggered_event(event_data: MessageCreatedEvent):
    """Handle a 'message_created' event.

    Args:
        event_data: The event data, represented as a Pydantic model instance.

    Returns:
        None.
    """

    logger.info("Received a 'webwidget_triggered' event: %s", event_data)
