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
    return f'{round(tournament.get_player_points(player) / tournament.get_games_count(),2)}'


@register.simple_tag
def get_player_200_points(player, tournament):
    player_points = tournament.get_player_points(player)
    result = player_points - (tournament.get_games_count() * 200) if player_points else 0
    return f'{round(result,2)}'


@register.filter
def get_item(dictionary, key):
    """
    Получение элемента из словаря по его ключу

    Args:
        dictionary (dict): Словарь, из которого необходимо получить элемент
        key: Ключ

    Returns:
        Элемент словаря dictionary[key]
    """
    return dictionary.get(key)
