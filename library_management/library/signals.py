from django.conf import settings
from django.core.mail import send_mail
from library.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def profile(sender, instance, created, **kwargs):
    if created:
        # sending email to the user
        subject = 'Welcome to Library Management System'
        message = f'Thank you {instance.username} for registration in Library Management System!!!'
        email_from = settings.EMAIL_HOST_USER
        recepient = [instance.email]
        send_mail(subject, message, email_from, recepient, fail_silently=False)
