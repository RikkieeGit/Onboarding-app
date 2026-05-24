from fastapi import APIRouter, HTTPException
from models.user import SignInRequest, RegisterRequest, VerifyRequest
from services import ad, sms

router = APIRouter()

@router.post("/signin")
async def signin(body: SignInRequest):
    # 1. Verify credentials against AD
    if not ad.verify_user(body.email, body.password):
        raise HTTPException(status_code=401, detail="Wrong email or password.")

    # 2. Get phone number from AD to send OTP
    phone = ad.get_user_phone(body.email)
    if not phone:
        raise HTTPException(status_code=400, detail="No phone number on file.")

    # 3. Send OTP
    sent = sms.send_otp(phone)
    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send OTP.")

    return { "message": "OTP sent.", "phone": phone }


@router.post("/register")
async def register(body: RegisterRequest):
    # 1. Check if user already exists
    if ad.user_exists(body.email):
        raise HTTPException(status_code=409, detail="Account already exists.")

    # 2. Send OTP to phone first — verify before creating AD account
    sent = sms.send_otp(body.phone)
    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send OTP.")

    return { "message": "OTP sent." }


@router.post("/verify")
async def verify(body: VerifyRequest):
    # 1. Check OTP with Twilio
    valid = sms.check_otp(body.phone, body.otp)
    if not valid:
        raise HTTPException(status_code=400, detail="Incorrect or expired code.")

    # 2. If signup flow — now create the AD user
    # Note: we need the registration data here, so the frontend
    # must resend it on verify for signup, or we store it temporarily.
    # For now we return success and handle AD creation separately.
    return { "message": "Verified." }
