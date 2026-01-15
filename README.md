# Lyftr Backend Assignment

This project implements a FastAPI-based webhook service that receives messages, verifies their authenticity, and stores them in a database with duplicate prevention.

## Features

- FastAPI webhook endpoint `/webhook`
- HMAC SHA-256 signature verification
- SQLite database storage
- Duplicate message detection
- Health check endpoints
- Proper error handling

---

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

---

## Installation

1. Clone the repository or extract the project folder.

2. Install dependencies:

pip install -r requirements.txt

3. Start the server:

uvicorn app.main:app --reload

---

## API Endpoints

### Health Endpoints

GET /  
Response: { "message": "App running" }

GET /health/live  
Response: { "status": "alive" }

GET /health/ready  
Response: { "status": "ready" }

---

### Webhook Endpoint

POST /webhook

Headers:

x-signature: <hmac_signature>

Example Request Body:

{
  "message_id": "123",
  "from": "+919876543210",
  "to": "+911234567890",
  "ts": "2025-01-18T12:00:00",
  "text": "hello"
}

---

## Response Types

### New Message

{
  "status": "ok",
  "result": "created"
}

### Duplicate Message

{
  "status": "ok",
  "result": "duplicate"
}



## How Signature Verification Works

The system verifies the request body using HMAC SHA-256 with a shared secret key stored in environment variable:

WEBHOOK_SECRET

If the signature does not match, the request is rejected with 401 Unauthorized.



## Database

- SQLite database is used
- Messages are stored uniquely using message_id
- Duplicate messages are ignored



