import os
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def send_activation_mail(request, player):
    # sending email
    current_site = get_current_site(request)
    mail_subject = 'Пожалуйста, подтвердите Ваш адрес электронной почты.'
    message = render_to_string('accounts/account_activate_email.html', {
        'user': player,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(player.user.pk)),
        'token': account_activation_token.make_token(player.user),
    })
    to_email = player.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    print(f"Email sent to {to_email}")


def filename(instance, filename):
    return os.path.join('passports', get_random_string(length=32) + '.' + filename.split('.')[-1])
