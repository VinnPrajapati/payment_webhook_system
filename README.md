# Payment Webhook System

A minimal webhook listener system built using FastAPI and PostgreSQL.

## Features

* Accepts payment webhook events
* Validates webhook signatures using HMAC SHA256
* Stores payment events in PostgreSQL
* Prevents duplicate event processing (idempotency)
* Provides API to fetch payment history
* Swagger API documentation

## Tech Stack

* Python 3.x
* FastAPI
* PostgreSQL
* SQLAlchemy
* Uvicorn

## Project Structure

```text
payment_webhook_system/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── webhook.py
│   └── utils.py
│
├── mock_payloads/
│   ├── payment_authorized.json
│   ├── payment_captured.json
│   └── payment_failed.json
│
├── create_tables.py
├── requirements.txt
├── README.md
├── DOCS.md
└── .env
```

## Installation

### Clone Repository

```bash
git clone <repository_url>
cd payment_webhook_system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE payment_webhook_db;
```

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/payment_webhook_db
WEBHOOK_SECRET=test_secret
```

Create tables:

```bash
python create_tables.py
```

## Run Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

## Testing Webhook

Generate signature using shared secret:

```text
test_secret
```

Send request:

```bash
curl --location 'http://localhost:8000/webhook/payments' \
--header 'Content-Type: application/json' \
--header 'X-Razorpay-Signature: <generated_signature>' \
--data '@mock_payloads/payment_authorized.json'
```

## Author
Vinod Kumar
