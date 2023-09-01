import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")

def send_email(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Mailgun Sandbox <postmaster@{domain}>",
              "to": to,
              "subject": subject,
              "text": body})

def send_registration_email(user):
    send_email(
        to=user.email,
        subject="Registration successful",
        body="You have successfully registered.",
    )