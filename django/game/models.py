from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User


# This is a player in a single game
class Player(models.Model):
    user = models.ForeignKey(User)
    icon = models.CharField(max_length=1)
    game = models.ForeignKey('Game')

    def __str__(self):
        return '%s as %s in %s' % (self.user.username, self.icon, self.game.name)


# This is a game session
class Game(models.Model):
    name = models.CharField(max_length=20, default='New game')

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
    won_by = models.ForeignKey('Player', related_name='games_won', null=True, blank=True)
    current_turn = models.ForeignKey('Player', related_name='current_turns', null=True, blank=True)

    def __str__(self):
        return 'Board for the game %s' % self.game.name

    def drop(self, player: Player, col: int, board: 'Board') -> 'Tile':
        # This method 'drops' a tile into the board

        print(self.current_turn)
        
        if ((self.current_turn != player) and (self.current_turn is not None)) or (self.game_status == 2):
            # This will happen when it's not the players turn
            raise Exception('It\'s not this players turn!')

        for row in range(1, self.height + 1):
            try:
                Tile.objects.get(position_x=col, position_y=row, board=board)
            except ObjectDoesNotExist as e:
                # This happens when it is empty. Place tile, switch user and exit
                tile = Tile(board=board, player=player, position_x=col, position_y=row)
                tile.save()

                self.current_turn = Player.objects.filter(game=self.game).exclude(pk=player.pk).get()
                self.save()

                return tile

        # This will happen when the column is completely filled
        raise Exception('Board seems to be full ...')

    def check_game_status(self, tile: 'Tile'):
        return


# These are the tiles placed on a specified board
class Tile(models.Model):
    board = models.ForeignKey('Board')
    player = models.ForeignKey('Player')
    position_x = models.IntegerField()
    position_y = models.IntegerField()

    class Meta:
        unique_together = ('position_x', 'position_y', 'board')

    def __str__(self):
        return 'Tile on Board %s from player %s on Position %s/%s' % (
            self.board.game.name, self.player.user.username, self.position_x, self.position_y)
