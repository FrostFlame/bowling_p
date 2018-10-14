from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import GameInfo


class GameResultUpdate(View):
    def post(self, request):
        game_info = get_object_or_404(GameInfo, pk=request.POST['info_id'])
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
