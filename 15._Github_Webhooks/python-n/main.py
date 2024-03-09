from fastapi import FastAPI, Request


app = FastAPI()


@app.post("/githubwebhookjson")
async def github_webhook(request: Request):
    print(await request.json())
    print(await request.body())

    return {"status": "ok"}


@app.post("/githubwebhookform")
async def github_webhook_form(request: Request):
    if request.headers.get("content-type") == "application/x-www-form-urlencoded":
        print(await request.form())
    return {"status": "ok"}
