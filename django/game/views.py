from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Player


def index(request):
    games = Game.objects.all()
    context = {
        'games': games,
    }
    return render(request, 'game/index.html', context)


def board(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    columns = range(1, game.board.width + 1)  # range wont include end value -> +1
    user = request.user
    context = {
        'user': user,
        'game': game,
        'columns': columns,
    }
    return render(request, 'game/board.html', context)


def drop_tile(request, game_id, column):
    game = get_object_or_404(Game, pk=game_id)
    player = Player.objects.get(user=request.user, game=game)

    game.board.drop(player, column, game.board)
    return redirect('game', game_id=game.pk)
