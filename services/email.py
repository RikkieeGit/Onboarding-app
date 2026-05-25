import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")

def send_otp_email(to_email: str, otp: str, name: str = "") -> bool:
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your verification code"
        msg["From"] = f"Paperwork <{SMTP_EMAIL}>"
        msg["To"] = to_email

        greeting = f"Hi {name}," if name else "Hi,"

        html = f"""
        <div style="font-family: 'Google Sans', Roboto, sans-serif; max-width: 480px; margin: 0 auto; padding: 40px 24px; background: #1e1f20; border-radius: 12px;">
            <p style="color: rgba(255,255,255,0.6); font-size: 14px; margin: 0 0 24px;">{greeting}</p>
            <p style="color: #e8eaed; font-size: 14px; margin: 0 0 32px;">
                Your verification code for Paperwork is:
            </p>
            <div style="background: #2a2b2c; border-radius: 8px; padding: 24px; text-align: center; margin-bottom: 32px;">
                <span style="font-size: 36px; font-weight: 500; color: #8ab4f8; letter-spacing: 8px;">{otp}</span>
            </div>
            <p style="color: rgba(255,255,255,0.4); font-size: 12px; margin: 0;">
                This code expires in 5 minutes. If you didn't request this, ignore this email.
            </p>
        </div>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())

        return True

    except Exception as e:
        print(f"[Email] Failed to send: {e}")
        return False
