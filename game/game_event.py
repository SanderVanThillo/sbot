class GameEvent:
    def __init__(self, message: str | None, board: str | None = None):
        self.__message = message
        self.__board = board

    def message(self) -> str:
        return self.__message

    def board(self) -> str:
        return self.__board