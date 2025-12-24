# backend/services/email/sender.py
# UTF-8, English only

def send_verification_email(email: str, verify_url: str):
    # MVP: console output only
    print("=== EMAIL VERIFICATION ===")
    print(f"To: {email}")
    print(f"Verify: {verify_url}")
    print("==========================")
