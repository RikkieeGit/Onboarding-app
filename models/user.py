from pydantic import BaseModel, EmailStr

class SignInRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class VerifyRequest(BaseModel):
    phone: str    # frontend sends email here despite the field name
    otp: str
    flow: str

class ForgotRequest(BaseModel):
    email: EmailStr
