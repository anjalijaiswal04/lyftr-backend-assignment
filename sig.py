import hmac
import hashlib

secret = "testsecret"

body = b'{"message_id":"123","from":"+919876543210","to":"+911234567890","ts":"2025-01-18T12:00:00","text":"hello"}'

signature = hmac.new(
    key=secret.encode(),
    msg=body,
    digestmod=hashlib.sha256
).hexdigest()

print("Generated Signature:")
print(signature)
