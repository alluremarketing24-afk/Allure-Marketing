from celery import shared_task
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_contact_email(subject, message, recipient_list):
    print("CELERY TASK: Sending email...")
    try:
        msg = EmailMultiAlternatives(subject, message, "your@email.com", recipient_list)
        msg.send()
        print("CELERY TASK: Email sent successfully.")
    except Exception as e:
        print(f"CELERY TASK FAILED: {e}")
