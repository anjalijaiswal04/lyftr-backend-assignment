import os
import hmac
import hashlib
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel, Field

from app.models import init_db
from app.storage import insert_message


os.environ["WEBHOOK_SECRET"] = "testsecret"
os.environ["DATABASE_URL"] = "sqlite:///app.db"


app = FastAPI()



# REQUEST BODY MODEL

class WebhookPayload(BaseModel):
    message_id: str
    from_: str = Field(..., alias="from")
    to: str
    ts: str
    text: Optional[str] = None

    class Config:
        populate_by_name = True



# STARTUP EVENT

@app.on_event("startup")
def startup_event():
    init_db()



# HEALTH ENDPOINTS

@app.get("/")
def root():
    return {"message": "App running"}


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    if not os.getenv("WEBHOOK_SECRET") or not os.getenv("DATABASE_URL"):
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"status": "ready"}



# HMAC SIGNATURE VERIFY

def verify_signature(secret: str, body: bytes, signature: str) -> bool:
    computed = hmac.new(
        key=secret.encode(),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed, signature)



# WEBHOOK ENDPOINT

@app.post("/webhook")
async def webhook(
    request: Request,
    payload: WebhookPayload,
    x_signature: str = Header(None)
):


    data = payload.dict(by_alias=True, exclude_none=True)

    result = insert_message(data)

    return {
        "status": "ok",
        "result": result
    }
