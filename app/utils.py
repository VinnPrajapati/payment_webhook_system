import hmac
import hashlib

def verify_signature(
    secret,
    payload,
    signature
):
    generated = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    print("=" * 50)
    print("Received :", signature)
    print("Generated:", generated)
    print("Payload   :", payload)
    print("=" * 50)

    return hmac.compare_digest(
        generated,
        signature
    )