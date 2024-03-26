from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post("/callback")
def callback(event: dict):
    print(f"Received event: {event}")
    return event


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=8001,
    )
