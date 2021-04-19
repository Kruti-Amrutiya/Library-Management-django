from celery import shared_task
from time import sleep
from django.core.mail import send_mail


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_task():
    sleep(10)
    send_mail("Celery Task Worked!",
    "This is the proof the task worked!",
    "krutiamrutiya1998@gmil.com",
    ["krutiamrutiya1998@gmail.com"])

    return None
