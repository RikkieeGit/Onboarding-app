import random
from datetime import datetime, timedelta

# In-memory store { email: { otp, expires_at } }
otp_store: dict = {}

def generate_otp(email: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_store[email] = {
        "otp": otp,
        "expires_at": datetime.now() + timedelta(minutes=5)
    }
    return otp

def verify_otp(email: str, code: str) -> bool:
    record = otp_store.get(email)
    if not record:
        return False
    if datetime.now() > record["expires_at"]:
        del otp_store[email]
        return False
    if record["otp"] != code:
        return False
    del otp_store[email]  # one-time use
    return True
