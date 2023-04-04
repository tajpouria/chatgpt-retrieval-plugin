from services.logger import logger


def process_unknown_event(agentbot_id: int, event_data: dict):
    """Handle an event with an unknown type.

    Args:
        event_data: The event data, represented as a dictionary.

    Returns:
        None.
    """
    logger.warning(
        "Agentbot %s Received an event with an unknown type: %s",
        agentbot_id,
        event_data.get("event"),
    )
