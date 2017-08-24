import game
import pytest

def trim_board(ascii_board):
    return '\n'.join([i.strip() for i in ascii_board.splitlines()])
t = trim_board

def test_new_board():
    assert game.Board(3,3).ascii() == t("""
    ...
    ...
    ...
    """)

    assert game.Board(4,3).ascii() == t("""
    ....
    ....
    ....
    """)

    assert game.Board(3,4).ascii() == t("""
    ...
    ...
    ...
    ...
    """)

def test_game():
    board = game.Board(3,3,win=3)
    assert board.count_tokens == 0
    assert board.game_status == 'active'
    assert board.turn_color is None
    # drop first token
    token = board.drop('x',0)
    assert board.game_status == 'active'
    assert token.position == (0,0)
    assert token.color == 'x'
    assert board.ascii() == t("""
    ...
    ...
    x..
    """)
    assert board.count_tokens == 1
    assert board.turn_color == 'o'
    # drop second token
    token = board.drop('o',0)
    assert board.game_status == 'active'
    assert token.position == (0,1)
    assert token.color == 'o'
    assert board.ascii() == t("""
    ...
    o..
    x..
    """)
    assert board.count_tokens == 2
    assert board.turn_color == 'x'

    # dropping the wrong color should raise an error
    with pytest.raises(Exception):
        token = board.drop('o',1)

    # drop third token
    token = board.drop('x',1)
    assert board.game_status == 'active'
    assert token.position == (1,0)
    assert token.color == 'x'
    assert board.ascii() == t("""
    ...
    o..
    xx.
    """)
    assert board.count_tokens == 3
    assert board.turn_color == 'o'
    # drop fourth token
    token = board.drop('o',0)
    assert board.game_status == 'active'
    assert token.position == (0,2)
    assert token.color == 'o'
    assert board.ascii() == t("""
    o..
    o..
    xx.
    """)
    assert board.count_tokens == 4

    # drop token on full column
    with pytest.raises(Exception):
        token = board.drop('x', 0)

    # drop fifth token
    token = board.drop('x',2)
    assert board.game_status == 'over'
    assert board.won_by == 'x'
    assert token.position == (2,0)
    assert token.color == 'x'
    assert board.ascii() == t("""
    o..
    o..
    xxx
    """)
    assert board.count_tokens == 5

    # drop token after game over
    with pytest.raises(Exception):
        token = board.drop('o', 2)

def test_load_board():
    """
    The Board class should provide a load method to load a predefined board.
    the load method should be implemented as a static method like this:

    >>> class Test:
    >>>     @staticmethod
    >>>     def a_static_factory():
    >>>        t = Test()
    >>>        # do something with t and return it
    >>>        return t

    the load function accepts a board layout. It retrieves the dimensions of the board
    and loads the provided data into the board.
    """

    board = game.Board.load(t("""
    o..
    o..
    xxx
    """))

def test_axis_strings():
    """
        There is one HUGE problem here. The method has no way to determine how many tiles it takes to win.
    """
    board = game.Board.load(t("""
    o..
    o...
    xxx
    """))

    # get the axis strings in this order:  | \ / -
    axis_strings = board.axis_strings(0,0)
    assert axis_strings[0] == 'xoo'
    assert axis_strings[1] == 'x'
    assert axis_strings[2] == 'x..'
    assert axis_strings[3] == 'xxx' # the winner :-)
