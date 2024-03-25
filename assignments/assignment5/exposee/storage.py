import sqlite3
from uuid import UUID, uuid4
from fastapi import Depends

from dtos import WebhookDTO, TicketDTO


def get_session() -> sqlite3.Connection:
    return sqlite3.connect("tickets.db", check_same_thread=False)


class TicketDAO:
    def __init__(self, db: sqlite3.Connection = Depends(get_session)):
        self.db = db
        self.session = db.cursor()

    def create_ticket(self, message: str) -> UUID:
        ticket_id = uuid4()
        self.session.execute(
            "INSERT INTO tickets (id, message) VALUES (?, ?)",
            (str(ticket_id), message),
        )
        self.db.commit()
        return ticket_id

    def close_ticket(self, ticket_id: UUID) -> None:
        self.session.execute(
            "DELETE FROM tickets WHERE id = ?",
            (str(ticket_id),),
        )
        self.db.commit()

    def update_ticket(self, ticket_id: UUID, message: str) -> None:
        self.session.execute(
            "UPDATE tickets SET message = ? WHERE id = ?",
            (message, str(ticket_id)),
        )
        self.db.commit()

    def ticket_exists(self, ticket_id: UUID) -> bool:
        return (
            self.session.execute(
                "SELECT COUNT(*) FROM tickets WHERE id = ?",
                (str(ticket_id),),
            ).fetchone()[0]
            > 0
        )

    def get_all_tickets(self) -> list[TicketDTO]:
        tickets = self.session.execute(
            "SELECT id, message FROM tickets",
        ).fetchall()
        return [TicketDTO(id=id, message=message) for id, message in tickets]


class WebhookDAO:
    def __init__(self, db: sqlite3.Connection = Depends(get_session)):
        self.db = db
        self.session = db.cursor()

    def create_webhook(self, url: str) -> UUID:
        webhook_id = uuid4()
        self.session.execute(
            "INSERT INTO webhooks (id, url) VALUES (?, ?)",
            (str(webhook_id), url),
        )
        self.db.commit()
        return webhook_id

    def delete_webhook(self, webhook_id: UUID) -> None:
        self.session.execute(
            "DELETE FROM webhooks WHERE id = ?",
            (str(webhook_id),),
        )
        self.db.commit()

    def webhook_exists(self, webhook_url: str) -> bool:
        return (
            self.session.execute(
                "SELECT COUNT(*) FROM webhooks WHERE url = ?",
                (webhook_url,),
            ).fetchone()[0]
            > 0
        )

    def get_webhook(self, webhook_id: UUID) -> str:
        return self.session.execute(
            "SELECT url FROM webhooks WHERE id = ?",
            (str(webhook_id),),
        ).fetchone()[0]

    def get_all_webhooks(self) -> list[WebhookDTO]:
        webhooks = self.session.execute(
            "SELECT id, url FROM webhooks",
        ).fetchall()
        return [WebhookDTO(id=id, url=url) for id, url in webhooks]
