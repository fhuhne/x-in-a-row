class Board:
    def __init__(self, width, height, win=4):
        self.width = width
        self.height = height
        self.win_length = win
        self.game_status = 'active'  # This is ok, you want to start with an active game
        self.won_by = None
        self.turn_color = None
        self.board = {}  # Create the Dict for the board
        self.count_tokens = self.count_tiles()  # Do the initial count to have the variable

        for x in range(self.width):
            self.board[x] = {}
            for y in range(self.height):
                self.board[x][y] = '.'

    def ascii(self):
        # This will go through the rows (y-axis) and print all the values for the according x-axis
        result = '\n'
        for y in reversed(range(self.height)):
            for x in range(self.width):
                result += self.board[x][y]
            result += '\n'

        return result

    def drop(self, player, col):
        # This method 'drops' the tile into the board

        if ((self.turn_color != player) and (self.turn_color is not None)) or (self.game_status == 'over'):
            # Raise an Exception when it's not the players turn or the game is over
            raise Exception

        for row in range(self.height):
            if self.board[col][row] == '.':
                self.board[col][row] = player

                # Switch the players around
                self.turn_color = 'o' if player == 'x' else 'x'
                # Check the games status
                self.game_status = self.check_game_status(Tile(player, (col, row)))  # Check game winning status
                # Count the tokens
                self.count_tokens = self.count_tiles()  # Count tiles currently on the board

                return Tile(player, (col, row))

        # This will happen when the column ist completely filled
        raise Exception

    def count_tiles(self):
        return sum(1 for col in self.board for row in self.board[col] if self.board[col][row] is not '.')

    def axis_strings(self, xc, yc):
        """
        We have the parameters for the coordinate of the tile we just placed.
        With this, we can check for a game win without checking every field on the board.
        """

        # This will preload the index so we don't have to do it before every direction
        axis_strings = {0: '', 1: '', 2: '', 3: ''}

        """
        Vertical
        """
        for y in range(self.height):
            axis_strings[0] += self.board[xc][y]

        """
        Diagonal 1
        """
        # Get the offset to the starting point. This will be the shorter axis.
        offset_d1 = xc if xc < self.height - yc - 1 else self.height - yc - 1

        # Get the max length for this diagonal. Add one because start is 0,0, but length should be 1 there.
        xl_d1 = self.width - (xc - offset_d1)  # Count how far we can go to the right (x-axis)
        yl_d1 = yc + offset_d1 + 1  # Count how far we can go down on the y-axis
        length_d1 = xl_d1 if xl_d1 < yl_d1 else yl_d1  # use the smaller one for the max length

        # go through the diagonal
        for position_d1 in range(length_d1):
            axis_strings[1] += self.board[xc - offset_d1 + position_d1][yc + offset_d1 - position_d1]

        """
        Diagonal 2
        Same logic as diagonal 1, but going up on the y-axis
        """
        offset_d2 = xc if xc < yc else yc

        xl_d2 = self.width - (xc - offset_d2)
        yl_d2 = self.height - (yc - offset_d2)
        length_d2 = xl_d2 if xl_d2 < yl_d2 else yl_d2

        for position_d2 in range(length_d2):
            axis_strings[2] += self.board[xc - offset_d2 + position_d2][yc - offset_d2 + position_d2]

        """
        Horizontal
        """
        for x in range(self.width):
            axis_strings[3] += self.board[x][yc]

        return axis_strings

    def check_game_status(self, tile):
        axis_strings = self.axis_strings(tile.position[0], tile.position[1])

        for axis in axis_strings:
            if tile.color * self.win_length in axis_strings[axis]:
                self.won_by = tile.color
                return 'over'

        return 'active'

    @staticmethod
    def load(board: str):
        rows = list(filter(None, board.splitlines()))

        """
            We take the "base row" and use this as the board width (columns).
            We do not check for errors in other rows except when there are too few entries.
            On longer rows entries are just ignored.
        """
        row_count = len(rows)
        col_count = len(rows[0])
        print('we have', row_count, 'rows')
        print('width is assumed to be', col_count, 'columns')

        game = Board(col_count, row_count)

        for y, row in enumerate(reversed(rows)):
            for x, char in enumerate(row):
                try:
                    game.board[x][y] = char
                except KeyError as error:
                    print('the board seems to be invalid', error)

        return game


class Tile:
    def __init__(self, color, position):
        self.color = color
        self.position = position
