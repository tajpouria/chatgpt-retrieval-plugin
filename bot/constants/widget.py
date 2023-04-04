from enum import Enum


class WidgetEventType(str, Enum):
    webwidget_triggered = "webwidget_triggered"
    message_created = "message_created"
