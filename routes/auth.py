from fastapi import APIRouter, HTTPException
from models.user import SignInRequest, RegisterRequest, VerifyRequest
from services import ad, otp, email

router = APIRouter()

# Temporary store for signup data until OTP verified
pending_registrations: dict = {}

@router.post("/register")
async def register(body: RegisterRequest):
    # Check if user already exists
    if ad.user_exists(body.email):
        raise HTTPException(status_code=409, detail="Account already exists.")

    # Generate and send OTP
    code = otp.generate_otp(body.email)
    sent = email.send_otp_email(body.email, code, body.name)
    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send email.")

    # Store registration data temporarily until OTP is verified
    pending_registrations[body.email] = {
        "name": body.name,
        "password": body.password,
    }

    return { "message": "OTP sent to your email." }


@router.post("/signin")
async def signin(body: SignInRequest):
    # Verify credentials against AD
    if not ad.verify_user(body.email, body.password):
        raise HTTPException(status_code=401, detail="Wrong email or password.")

    # Generate and send OTP
    code = otp.generate_otp(body.email)
    sent = email.send_otp_email(body.email, code)
    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send email.")

    return { "message": "OTP sent to your email." }


@router.post("/verify")
async def verify(body: VerifyRequest):
    # frontend sends email in the `phone` field
    email_addr = body.phone

    # Verify OTP
    valid = otp.verify_otp(email_addr, body.otp)
    if not valid:
        raise HTTPException(status_code=400, detail="Incorrect or expired code.")

    # If signup — create the AD user now
    if body.flow == "signup":
        reg = pending_registrations.get(email_addr)
        if not reg:
            raise HTTPException(status_code=400, detail="Registration session expired.")

        created = ad.create_user(
            name=reg["name"],
            email=email_addr,
            phone="",
            password=reg["password"]
        )
        if not created:
            raise HTTPException(status_code=500, detail="Failed to create account.")

        del pending_registrations[email_addr]

    return { "message": "Verified." }
