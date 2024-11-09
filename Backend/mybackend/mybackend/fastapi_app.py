# fastapi_app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/fastapi-hello")
async def hello_world():
    return {"message": "Hello from FastAP  I"}
