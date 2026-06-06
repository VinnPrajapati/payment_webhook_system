from fastapi import APIRouter
from fastapi import Request
from fastapi import Header
from fastapi import HTTPException
from app.utils import verify_signature
from app.database import SessionLocal
from app.models import PaymentEvent
from  app.logger import logger

router = APIRouter()

@router.post("/webhook/payments")
async def payment_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None)
):

    logger.info("2. Body received")

    raw_body = await request.body()

    if not x_razorpay_signature:
        raise HTTPException(
            status_code=403,
            detail="Missing signature"
        )

    if not verify_signature(
        "test_secret",
        raw_body,
        x_razorpay_signature
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid signature"
        )
   
    logger.info("3. Signature verified")

    try:
        payload = await request.json()

        logger.info("4. JSON parsed")

    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON"
        )

    event_id = payload["id"]

    event_type = payload["event"]

    payment_id = payload["payload"]["payment"]["entity"]["id"]

    db = SessionLocal()

    logger.info("5. DB session created")

    existing = db.query(
        PaymentEvent
    ).filter(
        PaymentEvent.event_id == event_id
    ).first()

    logger.info("6. Query executed")

    if existing:
        return {
            "message":
            "Event already processed"
        }

    event = PaymentEvent(
        event_id=event_id,
        payment_id=payment_id,
        event_type=event_type,
        payload=payload
    )

    db.add(event)
    db.commit()

    return {
        "message":
        "Webhook processed"
    }

@router.get("/payments/{payment_id}/events")
def get_events(payment_id: str):

    logger.info("1. Route Hit")

    db = SessionLocal()

    logger.info("2. DB Session Created")

    events = db.query(
        PaymentEvent
    ).filter(
        PaymentEvent.payment_id == payment_id
    ).order_by(
        PaymentEvent.received_at
    ).all()

    logger.info("3. Query Executed")

    return [
        {
            "event_type": e.event_type,
            "received_at": e.received_at
        }
        for e in events
    ]