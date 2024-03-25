from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID
from datetime import datetime
from typing import TypeVar, Generic
from typing import Annotated

from events import EventType


T = TypeVar("T", bound=BaseModel)


class CreatedResponse(BaseModel):
    id: UUID = Field(..., description="ID of the created object.")


class DefaultCreatedResponse(BaseModel):
    data: CreatedResponse
    success: bool = True
    message: str | None = "Object was created!"


class SuccessResponse(BaseModel):
    success: bool = True
    message: str | None = "Success!"


class WebhookDTO(BaseModel):
    id: UUID
    url: str


class TicketDTO(BaseModel):
    id: UUID
    message: str


class DataListResponse(BaseModel, Generic[T]):
    data: list[T]


class EventResponse(BaseModel):
    created: datetime
    event: EventType
    data: dict[str, str] | None = None


class RegisterWebhookRequest(BaseModel):
    callback_url: HttpUrl = Field(..., description="URL to register.")


class OpenTicketRequest(BaseModel):
    ticket_message: str = Field(..., description="Message of the ticket.")
