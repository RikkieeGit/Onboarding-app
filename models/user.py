from pydantic import BaseModel, EmailStr
from typing import Optional

class SignInRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class VerifyRequest(BaseModel):
    phone: str        # phone number OR email depending on flow
    otp: str
    flow: str         # "signin" or "signup"

class ForgotRequest(BaseModel):
    email: EmailStr
