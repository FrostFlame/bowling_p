from django import template

from accounts.models import RegistrationRequest
from tournaments.models import TournamentRequest

register = template.Library()


@register.simple_tag
def get_tournament_requests_count():
    return TournamentRequest.objects.get_active_requests().count()


@register.simple_tag
def get_registration_requests_count():
    return RegistrationRequest.objects.get_active_requests().count()
