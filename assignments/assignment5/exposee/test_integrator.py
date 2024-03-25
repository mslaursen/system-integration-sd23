from fastapi import FastAPI
import uvicorn
from typing import Any
from pydantic import BaseModel

app = FastAPI()


class EventRequest(BaseModel):
    created: Any
    event: Any


@app.post("/callback")
def callback(event: EventRequest):
    print(f"Received event: {event}")
    return event


if __name__ == "__main__":
    uvicorn.run(
        "test_integrator:app",
        reload=True,
        port=8001,
    )
