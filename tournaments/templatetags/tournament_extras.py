from django import template

register = template.Library()


@register.simple_tag
def get_player_points(player, tournament):
    return tournament.get_player_points(player)
