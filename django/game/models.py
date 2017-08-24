from django.db import models
from django.contrib.auth.models import User


# This is a game session
class Game(models.Model):
    name = models.CharField(max_length=20, default='New game')
    players = models.ManyToManyField(User)

    def __str__(self):
        return self.name


# This contains the state of the board
class Board(models.Model):
    GAME_STATUS_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active'),
        (2, 'Over'),
    )

    width = models.IntegerField(default=7)
    height = models.IntegerField(default=5)
    win_length = models.IntegerField(default=4)
    game_status = models.IntegerField(choices=GAME_STATUS_CHOICES, default=0)

    game = models.OneToOneField('Game')
    won_by = models.ForeignKey(User, related_name='games_won', null=True, blank=True)
    current_turn = models.ForeignKey(User, related_name='current_turns', null=True, blank=True)

    def __str__(self):
        return 'Board for the game %s' % self.game.name


# These are the tiles placed on a specified board
class Tile(models.Model):
    board = models.ForeignKey('Board')
    player = models.ForeignKey(User)
    position_x = models.IntegerField()
    position_y = models.IntegerField()

    class Meta:
        unique_together = ('position_x', 'position_y', 'board')

    def __str__(self):
        return 'Tile on Board %s from player %s on Position %s/%s' % (
            self.board.game.name, self.player.username, self.position_x, self.position_y)
