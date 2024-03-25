from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from storage import get_session
from routes import (
    webhook_router,
    ticket_router,
    service_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup db
    session = get_session()
    session.execute(
        "CREATE TABLE IF NOT EXISTS webhooks (id TEXT PRIMARY KEY, url TEXT)"
    )
    session.execute(
        "CREATE TABLE IF NOT EXISTS tickets (id TEXT PRIMARY KEY, message TEXT)"
    )

    app.include_router(webhook_router, prefix="/api/v1")
    app.include_router(ticket_router, prefix="/api/v1")
    app.include_router(service_router, prefix="/api/v1")
    yield
    # teardown db
    print("Shutting down db...")


app = FastAPI(
    title="Exposee webhook registration",
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=8000,
    )
