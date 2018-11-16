from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import GameInfo, TeamGameInfo


class GameResultUpdate(View):
    def post(self, request):
        team_type = request.POST['team_type']
        if team_type == 'solo':
            game_info = get_object_or_404(GameInfo, pk=request.POST['info_id'])
        else:
            game_info = get_object_or_404(TeamGameInfo, pk=request.POST['info_id'])
        game_result = request.POST['result']

        ctx = dict()
        if game_result.isdigit():
            game_info.point = game_result
            game_info.save(update_fields=['point'])
            ctx['Success'] = game_result
            ctx['id'] = game_info.id
        else:
            ctx['Error'] = 'Результат игры должен быть числом'

        return JsonResponse(ctx)
