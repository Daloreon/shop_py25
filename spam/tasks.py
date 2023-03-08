from django.core.mail import send_mail
from celery import shared_task
from spam.models import Contact

@shared_task
def send_spam():
    emails = [i.email for i in Contact.objects.all()]
    send_mail(
        'Py25 shop project', # title
        f'Привет загляни на наш сайт', # body
        'sovetbek.arnal52@gmail.com', # from
        emails # to
    )