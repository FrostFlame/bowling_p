from django import template

register = template.Library()


@register.simple_tag
def get_player_points(player, tournament):
    return tournament.get_player_points(player)


@register.simple_tag
def get_player_max_points(player, tournament):
    return tournament.get_player_max_points(player)


@register.simple_tag
def get_player_min_points(player, tournament):
    return tournament.get_player_min_points(player)


@register.simple_tag
def get_player_avg_points(player, tournament):
    return tournament.get_player_points(player) / tournament.games


@register.simple_tag
def get_player_200_points(player, tournament):
    return tournament.get_player_points(player) - (tournament.games * 200)


# todo add docstring
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
