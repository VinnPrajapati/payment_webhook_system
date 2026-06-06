# API Documentation

## Base URL

```text
http://localhost:8000
```

---

# Authentication

Webhook requests must include:

```http
X-Razorpay-Signature
```

The signature is validated using:

```text
HMAC SHA256
```

Shared Secret:

```text
test_secret
```

---

# 1. Receive Payment Webhook

## Endpoint

```http
POST /webhook/payments
```

## Headers

```http
Content-Type: application/json
X-Razorpay-Signature: <signature>
```

## Sample Request

```json
{
  "event": "payment.authorized",
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_014",
        "status": "authorized",
        "amount": 5000,
        "currency": "INR"
      }
    }
  },
  "created_at": 1751889865,
  "id": "evt_auth_014"
}
```

## Success Response

```json
{
  "message": "Webhook processed"
}
```

## Duplicate Event Response

```json
{
  "message": "Event already processed"
}
```

## Error Responses

### Invalid Signature

```json
{
  "detail": "Invalid signature"
}
```

Status Code:

```http
403 Forbidden
```

### Invalid JSON

```json
{
  "detail": "Invalid JSON"
}
```

Status Code:

```http
400 Bad Request
```

---

# 2. Fetch Payment Events

## Endpoint

```http
GET /payments/{payment_id}/events
```

## Example

```http
GET /payments/pay_014/events
```

## Success Response

```json
[
  {
    "event_type": "payment.authorized",
    "received_at": "2026-06-06T10:30:00"
  },
  {
    "event_type": "payment.captured",
    "received_at": "2026-06-06T10:35:00"
  }
]
```

## Response Fields

| Field       | Description                       |
| ----------- | --------------------------------- |
| event_type  | Type of payment event             |
| received_at | Timestamp when event was received |

---

# Event Storage

All webhook events are stored in PostgreSQL.

Stored Information:

* event_id
* payment_id
* event_type
* complete payload
* received_at

---

# Idempotency

The system ensures duplicate webhook events are not processed.

If an event with the same `event_id` already exists, it will be ignored.

---

# Supported Events

* payment.authorized
* payment.captured
* payment.failed
