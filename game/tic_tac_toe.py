import random

from game.game_event import GameEvent

TIC_TAC_TOE_DICT = {}
X_MARK = "X"
O_MARK = "O"
EMPTY_MARK = " "


def start_tic_tac_toe(player_id: str, player_mark: str) -> GameEvent:
    try:
        new_tic_tac_toe = TicTacToe(player_mark.upper())
        # if a game already exists for this player, it will be overwritten
        TIC_TAC_TOE_DICT[player_id] = new_tic_tac_toe

        if player_mark == O_MARK: new_tic_tac_toe.place_computer_mark()

        return GameEvent("Tic Tac Toe has started! X goes first.", str(new_tic_tac_toe))
    except InvalidMarkError as error:
        return GameEvent(error.message())


def play_tic_tac_toe(player_id: str, row: int, col: int) -> GameEvent:
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
        return GameEvent(error.message())


class TicTacToe:
    def __init__(self, player_mark: str):
        self.__board = [
            [EMPTY_MARK, EMPTY_MARK, EMPTY_MARK],
            [EMPTY_MARK, EMPTY_MARK, EMPTY_MARK],
            [EMPTY_MARK, EMPTY_MARK, EMPTY_MARK]
        ]
        if player_mark not in [X_MARK, O_MARK]: raise InvalidMarkError
        self.__player_mark = player_mark
        self.__computer_mark = O_MARK if player_mark == X_MARK else X_MARK

    def place_player_mark(self, row: int, col: int) -> None:
        if self.__board[row][col] != EMPTY_MARK: raise MarkedCellError
        self.__board[row][col] = self.__player_mark

    def place_computer_mark(self) -> None:
        if self.is_board_full(): raise FullBoardError

        is_computer_mark_placed = False
        while not is_computer_mark_placed:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.__board[row][col] == EMPTY_MARK:
                self.__board[row][col] = self.__computer_mark
                is_computer_mark_placed = True

    def is_board_full(self) -> bool:
        for row in self.__board:
            for col in row:
                if col == EMPTY_MARK:
                    return False
        return True

    def check_winner(self) -> str | None:
        # check rows
        for row in range(3):
            if self.__board[row][0] == self.__board[row][1] == self.__board[row][2] != EMPTY_MARK:
                return self.__create_winner_message(self.__board[row][0])

        # check columns
        for column in range(3):
            if self.__board[0][column] == self.__board[1][column] == self.__board[2][column] != EMPTY_MARK:
                return self.__create_winner_message(self.__board[0][column])

        # check diagonals
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2] != EMPTY_MARK:
            return self.__create_winner_message(self.__board[0][0])

        if self.__board[0][2] == self.__board[1][1] == self.__board[2][0] != EMPTY_MARK:
            return self.__create_winner_message(self.__board[0][2])

        if self.is_board_full():
            return self.__create_winner_message()

        return None

    def __create_winner_message(self, winner: str = "") -> str:
        if winner == self.__player_mark:
            return "Congratulations! You have won!"
        elif winner == self.__computer_mark:
            return "The computer has won!"
        else:
            return "It's a draw!"

    def __str__(self):
        return (f" {self.__board[0][0]} | {self.__board[0][1]} | {self.__board[0][2]} \n"
                "---|---|---\n"
                f" {self.__board[1][0]} | {self.__board[1][1]} | {self.__board[1][2]} \n"
                "---|---|---\n"
                f" {self.__board[2][0]} | {self.__board[2][1]} | {self.__board[2][2]} ")


class InvalidMarkError(Exception):

    def __init__(self):
        self.__message = "You can only choose X or O as your mark."
        super().__init__(self.__message)

    def message(self) -> str:
        return self.__message


class MarkedCellError(Exception):

    def __init__(self):
        self.__message = "This cell is already marked."
        super().__init__(self.__message)

    def message(self) -> str:
        return self.__message


class FullBoardError(Exception):

    def __init__(self):
        self.__message = "The board is full. No more moves can be made."
        super().__init__(self.__message)

    def message(self) -> str:
        return self.__message
