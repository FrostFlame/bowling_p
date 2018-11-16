from django import template

from tournaments.models import TeamType

register = template.Library()


@register.simple_tag
def get_game_info(tournament, player, game):
    result = game.point
    return result


@register.simple_tag
def get_team_game_info(tournament, team, game):
    if tournament.is_commercial():
        return sum(get_game_info(tournament, player, game.info.get(
            team=player.get_team(tournament, type=TeamType.objects.get(name='Один игрок')))) for player in
                   team.players.all())
    elif tournament.is_sport():
        return game.info.get(team=team).point


@register.simple_tag
def get_player_points(player, block):
    return block.get_player_points(player)


@register.simple_tag
def get_team_points(team, block):
    return sum(get_player_points(player, block) for player in team.players.all())


@register.simple_tag
def get_player_max_points(player, block):
    return block.get_player_max_points(player)


@register.simple_tag
def get_team_max_points(team, block):
    if block.games.all():
        return max(get_team_game_info(block.tournament, team, game) for game in block.games.all())
    else:
        return 0


@register.simple_tag
def get_player_min_points(player, block):
    return block.get_player_min_points(player)


@register.simple_tag
def get_team_min_points(team, block):
    if block.games.all():
        return min(get_team_game_info(block.tournament, team, game) for game in block.games.all())
    else:
        return 0


@register.simple_tag
def get_player_avg_points(player, block):
    if block.get_games_count() != 0:
        return f'{round(block.get_player_points(player) / block.get_games_count(),2)}'
    else:
        return 0


@register.simple_tag
def get_team_avg_points(team, block):
    if block.get_games_count() != 0:
        return f'{round(get_team_points(team, block) / block.get_games_count(),2)}'
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


@register.simple_tag
def get_team_handicap(games, team):
    if games:
        return len(games) * len(team.players.filter(sex='0')) * games[0].block.tournament.handicap_size
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
