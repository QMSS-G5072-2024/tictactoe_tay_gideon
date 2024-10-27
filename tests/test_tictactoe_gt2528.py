from tictactoe_gt2528 import tictactoe_gt2528
import pytest

def test_initialize_board():
    """
    Test to verify that initialize_board creates an 
    empty 3x3 board.
    """
    # Call the initialize_board function from tictactoe.py
    board = tictactoe_gt2528.initialize_board()

    # Check that the board has 3 rows
    actual_nrows = len(board)
    assert actual_nrows == 3, (
        f"Expected 3 rows, but got {len(board)} rows"
    )

    # Check that each row has 3 columns
    for row in board:
        actual_ncolumns = len(row)
        assert actual_ncolumns == 3, (
            f"Expected 3 columns in each row, " 
            f"but got {len(row)} columns"
        )
    
    # Check that all cells are initialized as empty spaces ' '
    assert all(cell == ' ' for row in board for cell in row), (
        "Some cells are not empty"
    )

# Create a list of all possible valid moves to test, 
# based on pre-specified board
@pytest.mark.parametrize("player, row, col", [
    ('X', 0, 1),  # Test move for 'X' at (0, 1)
    ('X', 0, 2),
    ('X', 1, 1),
    ('X', 1, 2),
    ('X', 2, 2),
    ('O', 0, 1),  # Test move for 'O' at (0, 1)
    ('O', 0, 2),
    ('O', 1, 1),
    ('O', 1, 2),
    ('O', 2, 2)
])
def test_make_move_valid(player, row, col):
    """
    Test that make_move successfully places a player's 
    symbol ('X' or 'O') on an empty cell in the Tic-Tac-Toe
    board, without affecting other cells.
    """
    # Create a pre-specified board configuration
    board = [
        ['X',' ',' '],
        ['O',' ',' '],
        ['X','O',' ']
    ]

    # Store a copy of the initial board for comparison
    # Deep copy of the board, cannot use .copy() as it makes shallow copy
    original_board = [row[:] for row in board]  

    # Make a valid move using make_move
    valid_move = tictactoe_gt2528.make_move(board, row, col, player)

    # Assert that the move was successful (return True)
    assert valid_move, (
        f"Move for player {player} at ({row}, {col}) "
        f"should be successful"
    )
    # Assert that player's symbol is added in the correct position
    assert board[row][col] == player, (
        f"Expected {player} at ({row}, {col}), "
        f"but got {board[row][col]}"
    )
    # Assert that no other cells are affected
    for i in range(3):
        for j in range(3):
            if (i, j) != (row, col):
                assert board[i][j] == original_board[i][j], (
                    f"Cell ({i}, {j}) should be unchanged, "
                    f"but got changed to {board[i][j]}"
                )

# Create a list of all possible invalid moves to test, 
# based on pre-specified board
@pytest.mark.parametrize("player, row, col", [
    ('X', 0, 0),  # Test move for 'X' at (0, 0)
    ('X', 1, 0),
    ('X', 2, 0),
    ('X', 2, 1),
    ('O', 0, 0),  # Test move for 'O' at (0, 0)
    ('O', 1, 0),
    ('O', 2, 0),
    ('O', 2, 1)
])
def test_make_move_invalid(player, row, col):
    """
    Test that make_move does not overwrite an occupied 
    cell and returns False when attempting to do so.
    """
    # Create a pre-specified board configuration
    board = [
        ['X',' ',' '],
        ['O',' ',' '],
        ['X','O',' ']
    ]

    # Create a deep copy of the original board to compare later
    original_board = [row[:] for row in board]

    # Make an invalid move using make_move
    invalid_move = tictactoe_gt2528.make_move(board, row, col, player)

    # Assert that the move will fail (return False)
    assert not invalid_move, (
        f"Move for player {player} at ({row}, {col}) "
        f"should fail as the cell is occupied"
    )
    # Assert that the board remains unchanged
    assert board == original_board, (
        "The board should remain unchanged after an invalid move"
    )

def test_game_integration():
    """
    Integration test that simulates an entire game, including:
    - Initializing the board
    - Making multiple moves
    - Checking for a winner
    - Resetting the game
    """
    # Step 1: Initialize the board
    board = tictactoe_gt2528.initialize_board()
    
    # Verify the initial board state (all cells should be empty)
    assert board == [[' ' for _ in range(3)] for _ in range(3)], (
        "Initial board should be empty"
    )
    
    # Step 2: Make multiple moves using the specified move sequence
    moves = [
        ('X', 0, 0),  # X move
        ('O', 0, 1),  # O move
        ('X', 1, 1),  # X move
        ('O', 0, 2),  # O move
        ('X', 2, 2)   # X winning move
    ]
    
    expected_board_states = [
        [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],  # After X at (0, 0)
        [['X', 'O', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],  # After O at (0, 1)
        [['X', 'O', ' '], [' ', 'X', ' '], [' ', ' ', ' ']],  # After X at (1, 1)
        [['X', 'O', 'O'], [' ', 'X', ' '], [' ', ' ', ' ']],  # After O at (0, 2)
        [['X', 'O', 'O'], [' ', 'X', ' '], [' ', ' ', 'X']]   # After X at (2, 2) - X wins
    ]
    
    expected_status = [None, None, None, None, 'X']  # No winner until the last move
    
    for i, (player, row, col) in enumerate(moves):
        # Make a move
        tictactoe_gt2528.make_move(board, row, col, player)

        # Step 3: Verify the state of the board after the move
        assert board == expected_board_states[i], (
            f"Board state after move {i+1} (Player {player}, {row}, {col}) is incorrect"
        )
        
        # Step 4: Check for winner or ongoing game status
        winner = tictactoe_gt2528.check_winner(board)
        assert winner == expected_status[i], (
            f"Game status after move {i+1} is incorrect: expected {expected_status[i]}, but got {winner}"
        )
    
    # Step 5: Reset the game
    board = tictactoe_gt2528.reset_game()
    
    # Step 6: Confirm the board is reset and there is no winner
    assert board == [[' ' for _ in range(3)] for _ in range(3)], "Board should be reset"
    assert tictactoe_gt2528.check_winner(board) is None, "There should be no winner after resetting the game"

@pytest.mark.parametrize(
    "initial_board, row, col, player, "
    "expected_result, expected_board",
    [
        # Test case 1: Empty board, valid moves for each cell (looped)
        # *[] unpacking operator to unpack results of list comprehension
        # into separate tuples for testing
        *[
            (
                # Initial empty board
                [[' ', ' ', ' '],  
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']],
                
                # Place 'X' on each valid position (r, c)
                r, c, 'X', True,
                
                # Expected board with 'X' in position (r, c)
                [
                    ['X' if (r == i and c == j) else ' ' for j in range(3)]  
                    for i in range(3)
                ]
            )

            # Loop over all valid positions (0,0) to (2,2)
            for r in range(3) for c in range(3) 
        ],

        # Test case 2: Occupied cell, move should fail
        (
            # Initial board where one cell is taken
            [['X', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']],
            
            # Move on the taken cell should return False
            0, 0, 'O', False,

            # Board should remain unchanged
            [['X', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
        ),

        # Test case 3: Valid move, place 'O' at (1, 1)
        (
            # Initial board
            [['X', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']],
            
            # Move on a valid, empty cell
            1, 1, 'O', True,
            
            # Expected board with 'O' at (1, 1)
            [['X', ' ', ' '],
             [' ', 'O', ' '],
             [' ', ' ', ' ']]
        ),

        # Test case 4: Out-of-bounds move (index too large), should raise IndexError
        (
            # Initial board
            [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']],
            
            # Move with too large index should raise error
            3, 3, 'X', pytest.raises(IndexError),

            # Board should remain unchanged
            [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
        )
    ]
)
def test_make_move(
    initial_board, row, col, player, 
    expected_result, expected_board
    ):
    """
    Test make_move's behaviour under different scenarios:
    1. Empty Board: A completely empty board where any 
    valid move should succeed.
    2. Occupied Cell: A board where one cell is already 
    taken. Making a move on that cell should returns False.
    3. Valid Move: A board where you attempt to place a 
    move on a valid, empty cell.
    4. Out-of-Bounds Moves: Consider moves where row or col 
    is outside the 3x3 grid. Should raise an IndexError.
    """
    # Test cases where an exception is expected (out-of-bounds moves)
    if isinstance(expected_result, type(pytest.raises(IndexError))):
        with expected_result:
            tictactoe_gt2528.make_move(
                initial_board, row, col, player
                )

    # Test cases where we check if the move was successful
    else:
        result = tictactoe_gt2528.make_move(
            initial_board, row, col, player
            )
        # Check if move was successful (or not) as expected
        assert result == expected_result, (
            f"Expected move result {expected_result}, "
            f"but got {result}"
        )
        # Check if board is updated correctly
        assert initial_board == expected_board, (
            f"Expected board:\n{expected_board}\n"
            f"But got:\n{initial_board}"
        )


# Set up an pre-defined board fixture to use in tests
@pytest.fixture
def set_board():
    """
    Fixture that provides a 3x3 Tic-Tac-Toe board with
    'X' placed at position (0, 0) before each test.
    """
    return [
        ['X', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
        ]

# Test for valid moves on this set board
@pytest.mark.parametrize(
    "player, row, col", [
        # Valid moves on the set board
        ('O', 0, 1),
        ('O', 0, 2),
        ('O', 1, 0),
        ('O', 1, 1),
        ('O', 1, 2),
        ('O', 2, 0),
        ('O', 2, 1),
        ('O', 2, 2)
    ]
)
def test_valid_moves_fixture(set_board, player, row, col):
    """
    Test valid moves using the set_board fixture.
    """
    valid_move = tictactoe_gt2528.make_move(set_board, row, col, player)
    # Assert that the move was successful (return True)
    assert valid_move, (
        f"Move for player {player} at ({row}, {col}) "
        f"should be successful"
    )
    # Assert that player's symbol is added in the correct position
    assert set_board[row][col] == player, (
        f"Expected {player} at ({row}, {col}), "
        f"but got {set_board[row][col]}"
    )

# Test on invalid out-of-bound moves on this board
@pytest.mark.parametrize(
    "player, row, col, expected_result", [
        # Invalid moves: out-of-bounds indices (should raise IndexError)
        ('X', 3, 0, pytest.raises(IndexError)),
        ('X', 0, 3, pytest.raises(IndexError))
    ]
)
def test_out_of_bounds_moves_fixture(
    set_board, player, row, col, expected_result
    ):
    """
    Test out-of-bounds moves that should raise an IndexError.
    """
    if isinstance(expected_result, type(pytest.raises(IndexError))):
        with expected_result:
            tictactoe_gt2528.make_move(set_board, row, col, player)

# Test invalid move on occupied cell
def test_occupied_cell_fixture(set_board):
    """
    Test trying to place a marker on an already occupied cell.
    """
    # Store a copy of the initial board for comparison
    original_board = [row[:] for row in set_board]

    # Try to place another move in the same spot
    result = tictactoe_gt2528.make_move(set_board, 0, 0, 'O')

    # Assert invalid move fails
    assert result is False, (
        "Expected move to fail because the cell is occupied."
    )
    # Assert board is unchanged
    assert set_board == original_board, (
        "The board should not change with invalid move."
    )

# List a variety of board layouts and expected results
@pytest.mark.parametrize(
    "board, expected_result", [
        (
            # Case of Draw (no more possible moves)
            [['O', 'X', 'X'],
             ['X', 'O', 'O'],
             ['O', 'X', 'X']], # Board to test
            'Draw'             # Expected result (Draw)
        ),
        (
            # Case of X winning
            [['X', 'O', ' '],
             ['X', ' ', ' '],
             ['X', 'O', ' ']], # Board to test
            'X'                # Expected result (X win)
        ),
        (
            # Case of O winning
            [['O', 'O', 'O'],
             ['X', ' ', ' '],
             ['X', ' ', 'X']], # Board to test
            'O'                # Expected result (O win)
        ),
        (
            # Case of ongoing game (a winner is still possible)
            [['O', ' ', 'O'],
             ['X', ' ', ' '],
             ['X', ' ', ' ']], # Board to test
            None               # Expected result (ongoing game)
        ),
        (
            # Case of ongoing game (no way for any player
            # to win but valid moves still possible)
            [['O', 'X', 'X'],
             ['X', 'O', 'O'],
             ['O', 'X', ' ']], # Board to test
            None               # Expected result (ongoing game)
        )
    ]
)
def test_check_winner(board, expected_result):
    """
    Test check_winner's ability to identify 
    wins, draws, and ongoing games.
    """
    # Check the board's outcome
    result = tictactoe_gt2528.check_winner(board)
    # Assert that result should be as expected
    assert result == expected_result, (
        f"We expect check_winner to return {expected_result}, "
        f"but it returns {result}"
    )