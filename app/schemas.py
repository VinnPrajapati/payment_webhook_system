from pydantic import BaseModel


class WebhookPayload(BaseModel):
    event: str
    payload: dict
    created_at: int
    id: str