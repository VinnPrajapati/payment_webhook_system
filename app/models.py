from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.database import Base

class PaymentEvent(Base):

    __tablename__ = "payment_events"

    id = Column(Integer, primary_key=True)

    event_id = Column(String, unique=True, nullable=False)

    payment_id = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    payload = Column(JSON)

    received_at = Column(DateTime, default=datetime.utcnow)

