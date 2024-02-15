from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def _():
    return {"message": "Hello World"}


@app.get("/1")
def _():
    return {"message": "Hello World"}


@app.get("/firstroute")
def first_route():
    return {"message": "Hello World"}
