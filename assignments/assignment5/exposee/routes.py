from fastapi import Query, APIRouter, Depends
from fastapi.exceptions import HTTPException
from uuid import UUID
import requests
from datetime import datetime, timezone

from events import EventType
from storage import TicketDAO, WebhookDAO, get_session
from dtos import (
    DefaultCreatedResponse,
    CreatedResponse,
    EventResponse,
    SuccessResponse,
    DataListResponse,
    WebhookDTO,
    RegisterWebhookRequest,
    OpenTicketRequest,
    TicketDTO,
)


webhook_router = APIRouter(prefix="/webhooks", tags=["webhooks"])
ticket_router = APIRouter(prefix="/tickets", tags=["tickets"])
service_router = APIRouter(prefix="/service", tags=["service"])


def _send_event(
    event: EventType,
    data: dict[str, str] | None = None,
) -> None:
    """Send event to all registered webhooks."""
    dao = WebhookDAO(db=get_session())

    body = EventResponse(
        event=event,
        created=datetime.now(timezone.utc),
        data=data,
    )

    for webhook in dao.get_all_webhooks():
        try:
            requests.post(
                webhook.url,
                data=body.model_dump_json(),
                timeout=2,
            )
        except requests.exceptions.RequestException:
            pass


#
# Webhook routes
#


@webhook_router.post("/register", status_code=201)
def register_webhook(
    request_dto: RegisterWebhookRequest,
    dao: WebhookDAO = Depends(),
) -> DefaultCreatedResponse:
    """Register callback url in database."""

    webhook = str(request_dto.callback_url)
    if dao.webhook_exists(webhook):
        raise HTTPException(
            status_code=400,
            detail="Webhook already exists.",
        )

    obj_id = dao.create_webhook(webhook)
    return DefaultCreatedResponse(data=CreatedResponse(id=obj_id))


@webhook_router.delete("/unregister/{webhook_id}")
def unregister_webhook(
    webhook_id: UUID,
    dao: WebhookDAO = Depends(),
) -> SuccessResponse:
    """Unregister callback url from database."""

    if not dao.get_webhook(webhook_id):
        raise HTTPException(
            status_code=404,
            detail="Webhook not found.",
        )

    dao.delete_webhook(webhook_id)
    return SuccessResponse()


@webhook_router.get("")
def get_all_webhooks(
    dao: WebhookDAO = Depends(),
) -> DataListResponse[WebhookDTO]:
    """Get all registered webhooks."""

    return DataListResponse(
        data=dao.get_all_webhooks(),
    )


@webhook_router.post("/ping")
def ping_all_webhooks() -> SuccessResponse:
    """Ping all registered webhooks."""

    _send_event(EventType.ping)
    return SuccessResponse()


#
# Ticket routes
#


@ticket_router.post("", status_code=201)
def open_ticket(
    request_dto: OpenTicketRequest,
    dao: TicketDAO = Depends(),
) -> DefaultCreatedResponse:
    """Create/Open a ticket."""

    obj_id = dao.create_ticket(request_dto.ticket_message)

    _send_event(
        EventType.ticket_opened,
        data=request_dto.model_dump(),
    )
    return DefaultCreatedResponse(data=CreatedResponse(id=obj_id))


@ticket_router.delete("/{ticket_id}")
def close_ticket(
    ticket_id: UUID,
    dao: TicketDAO = Depends(),
) -> SuccessResponse:
    """Close/Delete a ticket."""

    if not dao.ticket_exists(ticket_id):
        raise HTTPException(
            status_code=404,
            detail="Ticket not found.",
        )

    dao.close_ticket(ticket_id)
    _send_event(EventType.ticket_closed)
    return SuccessResponse()


@ticket_router.patch("/{ticket_id}")
def update_ticket(
    ticket_id: UUID,
    update_dto: OpenTicketRequest,
    dao: TicketDAO = Depends(),
) -> SuccessResponse:
    """Update a ticket."""

    if not dao.ticket_exists(ticket_id):
        raise HTTPException(
            status_code=404,
            detail="Ticket not found.",
        )

    dao.update_ticket(ticket_id, update_dto.ticket_message)
    _send_event(
        EventType.ticket_updated,
        data=update_dto.model_dump(),
    )
    return SuccessResponse()


@ticket_router.get("")
def get_all_tickets(
    dao: TicketDAO = Depends(),
) -> DataListResponse[TicketDTO]:
    """Get all tickets."""

    return DataListResponse(
        data=dao.get_all_tickets(),
    )


#
# Service routes
#


@service_router.post("/unavailable")
def service_unavailable() -> SuccessResponse:
    """Set service to unavailable."""

    _send_event(EventType.service_unavailable)
    return SuccessResponse()


@service_router.post("/available")
def service_available() -> SuccessResponse:
    """Set service to available."""

    _send_event(EventType.service_available)
    return SuccessResponse()
