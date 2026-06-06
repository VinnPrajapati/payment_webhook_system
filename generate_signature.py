import hmac
import hashlib

secret = "test_secret"

with open(
    "mock_payloads/payment_authorized.json",
    "rb"
) as f:
    body = f.read()

signature = hmac.new(
    secret.encode(),
    body,
    hashlib.sha256
).hexdigest()

print(signature)