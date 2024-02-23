from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/fastapiData")
def serve_data():
    return {"message": [1, 2, 3, 4, 5]}


@app.get("/requestExpress")
def request_express():
    url = "http://localhost:7070/expressData"
    response = requests.get(url)

    return response.json()
