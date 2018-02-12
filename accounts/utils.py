import os
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail


def send_activation_mail(request, player):
    current_site = get_current_site(request)
    mail_subject = 'Пожалуйста, подтвердите Ваш адрес электронной почты.'
    message = render_to_string('accounts/account_activate_email2.html', {
        'user': player,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(player.user.pk)),
        'token': account_activation_token.make_token(player.user),
    })
    to_email = player.user.email
    send_mail(
        mail_subject, message, 'tatar.bowling@gmail.com', [to_email], html_message=message,
    )


def filename(instance, filename):
    return os.path.join('passports', get_random_string(length=32) + '.' + filename.split('.')[-1])
