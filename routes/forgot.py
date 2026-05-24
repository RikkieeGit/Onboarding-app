from fastapi import APIRouter, HTTPException
from models.user import ForgotRequest
from services import ad, sms

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(body: ForgotRequest):
    phone = ad.get_user_phone(body.email)
    if not phone:
        # Don't reveal if email exists — security best practice
        return { "message": "If that email exists, a code has been sent." }

    sms.send_otp(phone)
    return { "message": "If that email exists, a code has been sent." }
