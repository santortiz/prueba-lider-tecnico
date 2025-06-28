import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Personalization
from app.config import get_settings

settings = get_settings()

def send_email(to_email: str):
    
    message = Mail()
    message.from_email = Email(settings.FROM_EMAIL)
    message.subject = "Confirmación de Reserva"
    message.template_id = settings.TEMPLATE_ID

    personalization = Personalization()
    personalization.add_to(To(to_email))
    message.add_personalization(personalization)

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email} with status: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
