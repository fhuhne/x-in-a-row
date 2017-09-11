from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Player


def index(request):
    """
    Overview with all active games
    """
    games = Game.objects.exclude(board__game_status='2')
    context = {
        'games': games,
    }
    return render(request, 'game/index.html', context)


def board(request, game_id):
    """
    Display the board
    """
    game = get_object_or_404(Game, pk=game_id)
    columns = range(1, game.board.width + 1)  # range wont include end value -> + 1
    user = request.user
    context = {
        'user': user,
        'game': game,
        'columns': columns,
    }
    return render(request, 'game/board.html', context)


def drop_tile(request, game_id, column):
    """
    Handle the tile drop logic. No view, redirect to the current board
    """
    game = get_object_or_404(Game, pk=game_id)
    player = Player.objects.get(user=request.user, game=game)

    game.board.drop(player, column, game.board)
    return redirect('game', game_id=game.pk)
