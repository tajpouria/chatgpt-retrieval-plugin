from fastapi import APIRouter
from bot.constants.widget import WidgetEventType
from bot.services.process_message_created_event import (
    process_message_created_event,
)
from bot.services.process_unknown_event import process_unknown_event
from bot.services.process_webwidget_triggered_event import (
    process_webwidget_triggered_event,
)


router_v1 = APIRouter()


@router_v1.post("/widget-event")
async def handle_widget_event(request: dict):
    """Handle incoming widget events.

    Args:
        request: The request body, which should contain an 'event' property indicating the type
            of event being handled, as well as additional properties specific to that event type.

    Returns:
        A dictionary with a 'status' property indicating the success or failure of the event handling.
    """
    event_type = WidgetEventType(request.get("event"))
    if event_type == WidgetEventType.webwidget_triggered:
        # Handle the 'webwidget_triggered' event
        process_webwidget_triggered_event(request)
    elif event_type == WidgetEventType.message_created:
        # Handle the 'message_created' event
        process_message_created_event(request)
    else:
        # Handle unknown event types
        process_unknown_event(request)

    return {"status": "success"}
