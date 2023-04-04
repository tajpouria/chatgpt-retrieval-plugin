from services.logger import logger


def process_unknown_event(event_data: dict):
    """Handle an event with an unknown type.

    Args:
        event_data: The event data, represented as a dictionary.

    Returns:
        None.
    """
    logger.warning(
        "Received an event with an unknown type: %s", event_data.get("event")
    )
