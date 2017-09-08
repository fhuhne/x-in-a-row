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

                self.check_game_status(tile)
                if self.game_status != 2:
                    self.current_turn = Player.objects.filter(game=self.game).exclude(pk=player.pk).get()

                self.save()

                return tile

        # This will happen when the column is completely filled
        raise Exception('Board seems to be full ...')

    def check_game_status(self, tile: 'Tile'):
        axis_strings = self.axis_strings(tile.position_x, tile.position_y)

        for axis in axis_strings:
            last_player = None
            count = 1

            for index, tile in enumerate(axis_strings[axis]):
                if tile:
                    if last_player == tile.player:
                        count += 1
                    else:
                        count = 1

                    if count >= self.win_length:
                        self.game_status = 2
                        self.won_by = tile.player

                    last_player = tile.player
                else:
                    count = 1
                    last_player = None

    def axis_strings(self, xc: int, yc: int):
        """
        We have the parameters for the coordinate of the tile we just placed.
        With this, we can check for a game win without checking every field on the board.
        """
        xc = int(xc)
        yc = int(yc)

        # This will preload the index so we don't have to do it before every direction
        axis_strings = {0: [], 1: [], 2: [], 3: []}

        """
        Vertical
        """
        for index in range(1, self.height + 1):
            try:
                tile = self.tile_set.get(position_x=xc, position_y=index)
                axis_strings[0].append(tile)
            except ObjectDoesNotExist:
                axis_strings[0].append(None)

        # print(axis_strings[0])

        """
        Diagonal 1 -> left top going bottom right
        """
        # Get the offset to the starting point. This will be the shorter axis.
        offset_d1 = xc - 1 if xc - 1 < self.height - yc else self.height - yc

        # Get the max length for this diagonal.
        xl_d1 = self.width - (xc - offset_d1)  # Count how far we can go to the right (x-axis)
        yl_d1 = yc + offset_d1  # Count how far we can go down on the y-axis
        length_d1 = xl_d1 if xl_d1 < yl_d1 else yl_d1  # use the smaller one for the max length

        # go through the diagonal
        for position_d1 in range(length_d1):
            # axis_strings[1] += self.board[xc - offset_d1 + position_d1][yc + offset_d1 - position_d1]
            try:
                tile = self.tile_set.get(
                    position_x=(xc - offset_d1 + position_d1),
                    position_y=(yc + offset_d1 - position_d1)
                )
                axis_strings[1].append(tile)
            except ObjectDoesNotExist:
                axis_strings[1].append(None)

        """
        Diagonal 2
        Same logic as diagonal 1, but going up on the y-axis
        """
        offset_d2 = xc - 1 if xc - 1 < yc - 1 else yc - 1

        xl_d2 = self.width - (xc - offset_d2)
        yl_d2 = self.height - (yc - offset_d2)
        length_d2 = xl_d2 if xl_d2 < yl_d2 else yl_d2

        for position_d2 in range(length_d2):
            # axis_strings[2] += self.board[xc - offset_d2 + position_d2][yc - offset_d2 + position_d2]
            try:
                tile = self.tile_set.get(
                    position_x=(xc - offset_d2 + position_d2),
                    position_y=(yc - offset_d2 + position_d2)
                )
                axis_strings[2].append(tile)
            except ObjectDoesNotExist:
                axis_strings[2].append(None)

        """
        Horizontal
        """
        for index in range(1, self.width + 1):
            try:
                tile = self.tile_set.get(position_x=index, position_y=yc)
                axis_strings[3].append(tile)
            except ObjectDoesNotExist:
                axis_strings[3].append(None)

        return axis_strings


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
