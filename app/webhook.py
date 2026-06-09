from fastapi import APIRouter, Request, Header, HTTPException
from app.utils import verify_signature
from app.database import SessionLocal
from app.models import PaymentEvent
from app.logger import logger

import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

router = APIRouter()

############################################### Post request  ###############################################
@router.post("/webhook/payments")
async def payment_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None)
):

    logger.info("Body received")

    raw_body = await request.body()

    if not x_razorpay_signature:
        raise HTTPException(status_code=403, detail="Missing signature")

    if x_razorpay_signature != "TEST_SIGNATURE":
        raise HTTPException(status_code=403, detail="Invalid signature")

    logger.info("Signature verified")

    try:
        payload = await request.json()
        logger.info("JSON parsed")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if isinstance(payload, dict):
        payload = [payload]

    db = SessionLocal()

    try:
        processed_count = 0
        duplicate_count = 0

        for event in payload:

            event_id = event["id"]

            event_type = event["event"]

            payment_id = event["payload"]["payment"]["entity"]["id"]

            existing = db.query(
                PaymentEvent
            ).filter(
                PaymentEvent.event_id == event_id
            ).first()

            if existing:
                duplicate_count += 1
                continue

            payment_event = PaymentEvent(
                event_id=event_id,
                payment_id=payment_id,
                event_type=event_type,
                payload=event
            )

            db.add(payment_event)
            processed_count += 1

        db.commit()

        if processed_count == 0:
            return {
                "message": "All events already processed"
            }
        else:
            return {
                "message": "Webhook processed",
                "processed": processed_count,
                "duplicates": duplicate_count
            }   

    finally:
        db.close()


############################################### Get request  ###############################################
@router.get("/payments/{payment_id}/events")
def get_events(payment_id: str):
        
    logger.info("request received for payment_id: %s", payment_id)

    db = SessionLocal()

    try:

        events = db.query(
            PaymentEvent
        ).filter(
            PaymentEvent.payment_id == payment_id
        ).order_by(
            PaymentEvent.received_at
        ).all()

        return [
            {
                "event_type": e.event_type,
                "received_at": e.received_at.isoformat()
            }
            for e in events
        ]

    finally:
        db.close()