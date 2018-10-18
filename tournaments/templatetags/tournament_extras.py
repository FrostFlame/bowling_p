from django import template

register = template.Library()

@register.simple_tag
def get_game_info(tournament, player, game):
    result = game.point
    if tournament.handicap and result != 0 and (player.sex == '0' or player.get_age() >= 50):
        result += tournament.handicap_size
    return result

@register.simple_tag
def get_player_points(player, block):
    return block.get_player_points(player)


@register.simple_tag
def get_player_max_points(player, block):
    return block.get_player_max_points(player)


@register.simple_tag
def get_player_min_points(player, block):
    return block.get_player_min_points(player)


@register.simple_tag
def get_player_avg_points(player, block):
    if block.get_games_count() != 0:
        return f'{round(block.get_player_points(player) / block.get_games_count(),2)}'
    else:
        return 0


@register.simple_tag
def get_player_200_points(player, block):
    player_points = block.get_player_points(player)
    # games_count = tournament.get_games_count()
    result = player_points - (block.get_games_count() * 200) if player_points else 0
    return f'{round(result,2)}'


@register.simple_tag
def get_sum(a, b):
    return f'{a + b}'


@register.simple_tag
def get_handicap(games_list, tournament):
    if games_list is not None:
        gk = list(filter(lambda x: x.point != 0, games_list))
        return f'{len(gk) * tournament.handicap_size}'
    else:
        return 0


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


@register.filter
def get_list_len(list):
    """
    Получение количества ключей в словера

    Args:
        list (list)

    Returns:
        Количество ключей в словаре dictionary
    """
    return len(list)
