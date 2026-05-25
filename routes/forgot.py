from fastapi import APIRouter
from models.user import ForgotRequest
from services import ad, otp, email

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(body: ForgotRequest):
    # Don't reveal if email exists — security best practice
    exists = ad.user_exists(body.email)
    if exists:
        code = otp.generate_otp(body.email)
        email.send_otp_email(body.email, code)
    return { "message": "If that email exists, a reset code has been sent." }
