from enum import Enum


class EventType(Enum):
    """Event types."""

    ticket_opened = "ticket_opened"
    ticket_closed = "ticket_closed"
    ticket_updated = "ticket_updated"
    service_unavailable = "service_unavailable"
    service_available = "service_available"
    ping = "ping"
