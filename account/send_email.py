from django.core.mail import send_mail

def send_activation_code(email, code):
    send_mail(
        'Py25 shop project', # title
        f'http://localhost:8000/api/v1/account/activate/{code}', # body
        'vladislav001015@gmail.com', # from
        [email] # to
    )

def send_reset_password_code(email, code):
    send_mail(
        'Py25 shop project', # title
        f'привет чтобы бросить пароль тебе нужно знать этот код = {code}', # body
        'vladislav001015@gmail.com', # from
        [email] # to
    )