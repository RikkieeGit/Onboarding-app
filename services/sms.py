import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)
VERIFY_SID = os.getenv("TWILIO_VERIFY_SID")

def send_otp(phone: str) -> bool:
    """Send OTP via Twilio Verify to a phone number or email."""
    try:
        client.verify.v2.services(VERIFY_SID) \
            .verifications.create(to=phone, channel="sms")
        return True
    except Exception as e:
        print(f"[Twilio] Failed to send OTP: {e}")
        return False

def check_otp(phone: str, code: str) -> bool:
    """Verify OTP code via Twilio Verify."""
    try:
        result = client.verify.v2.services(VERIFY_SID) \
            .verification_checks.create(to=phone, code=code)
        return result.status == "approved"
    except Exception as e:
        print(f"[Twilio] Failed to verify OTP: {e}")
        return False
