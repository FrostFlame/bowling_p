from django import template

register = template.Library()


@register.simple_tag
def get_rating_points(tournament, player):
    return tournament.get_rating_points(player)
