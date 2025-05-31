import random

from game.game_event import GameEvent

TIC_TAC_TOE_DICT = {}
X_MARK = 'X'
O_MARK = 'O'
EMPTY_MARK = ' '


def start(player_id: str, player_mark: str) -> GameEvent:
    try:
        new_tic_tac_toe = TicTacToe(player_mark.upper())
        # if a game already exists for this player, it will be overwritten
        TIC_TAC_TOE_DICT[player_id] = new_tic_tac_toe

        if player_mark == O_MARK: new_tic_tac_toe.place_computer_mark()
    
        return GameEvent('Tic Tac Toe has started! X goes first.', str(new_tic_tac_toe))
    except InvalidMarkError as error:
        return GameEvent(error.message)


def play(player_id: str, row: int, col: int) -> GameEvent:
    try:
        tic_tac_toe = TIC_TAC_TOE_DICT[player_id]

        tic_tac_toe.place_player_mark(row, col)
        winner = tic_tac_toe.check_winner()
        if winner:
            board = str(tic_tac_toe)
            del TIC_TAC_TOE_DICT[player_id]
            return GameEvent(winner, board)

        tic_tac_toe.place_computer_mark()
        winner = tic_tac_toe.check_winner()
        if winner:
            board = str(tic_tac_toe)
            del TIC_TAC_TOE_DICT[player_id]
            return GameEvent(winner, board)

        return GameEvent("Next round!", str(tic_tac_toe))
    except KeyError:
        return GameEvent("Tic Tac Toe game not yet started")
    except MarkedCellError as error:
        return GameEvent(error.message)


class TicTacToe:
    def __init__(self, player_mark: str):
        self.board = [
            [EMPTY_MARK, EMPTY_MARK, EMPTY_MARK], 
            [EMPTY_MARK, EMPTY_MARK, EMPTY_MARK], 
            [EMPTY_MARK, EMPTY_MARK, EMPTY_MARK]
        ]
        if player_mark not in [X_MARK, O_MARK]: raise InvalidMarkError
        self.player_mark = player_mark
        self.computer_mark = O_MARK if player_mark == X_MARK else X_MARK

    def place_player_mark(self, row: int, col: int) -> None:
        if self.board[row][col] != EMPTY_MARK: raise MarkedCellError
        self.board[row][col] = self.player_mark

    def place_computer_mark(self) -> None:
        if self.is_board_full(): raise FullBoardError

        is_computer_mark_placed = False
        while not is_computer_mark_placed:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.board[row][col] == EMPTY_MARK:
                self.board[row][col] = self.computer_mark
                is_computer_mark_placed = True

    def is_board_full(self) -> bool:
        for row in self.board:
            for col in row:
                if col == EMPTY_MARK:
                    return False
        return True

    def check_winner(self) -> str | None:
        # check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != EMPTY_MARK:
                return self.__create_winner_message(self.board[row][0])

        # check columns
        for column in range(3):
            if self.board[0][column] == self.board[1][column] == self.board[2][column] != EMPTY_MARK:
                return self.__create_winner_message(self.board[0][column])

        # check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY_MARK:
            return self.__create_winner_message(self.board[0][0])

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY_MARK:
            return self.__create_winner_message(self.board[0][2])

        if self.is_board_full():
            return self.__create_winner_message()

        return None

    def __create_winner_message(self, winner: str = "") -> str:
        if winner == self.player_mark:
            return "Congratulations! You have won!"
        elif winner == self.computer_mark:
            return "The computer has won!"
        else:
            return "It's a draw!"

    def __str__(self):
        return (f" {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]} \n"
                "---|---|---\n"
                f" {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]} \n"
                "---|---|---\n"
                f" {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]} ")


class InvalidMarkError(Exception):

    def __init__(self):
        self.message = "You can only choose X or O as your mark."
        super().__init__(self.message)


class MarkedCellError(Exception):

    def __init__(self):
        self.message = "This cell is already marked."
        super().__init__(self.message)

class FullBoardError(Exception):

    def __init__(self):
        self.message = "The board is full. No more moves can be made."
        super().__init__(self.message)