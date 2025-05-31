class GameEvent:
    def __init__(self, message: str | None, board: str | None = None):
        self.message = message
        self.board = board