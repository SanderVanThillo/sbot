import requests

from game.game_event import GameEvent

HANGMAN_DICT = {}

def start_hangman(player_id: str) -> GameEvent:
    try:
        random_word = requests.get("https://random-word-api.vercel.app/api?words=1").json()[0]

        new_hangman = Hangman(random_word)
        HANGMAN_DICT[player_id] = new_hangman

        return GameEvent("Hangman has started! Make you first guess!", new_hangman.create_board())
    except:
        return GameEvent("Hangman game could not be started!")

def guess_hangman(player_id: str, guess: str) -> GameEvent:
    try:
        hangman = HANGMAN_DICT[player_id]
        message = hangman.do_guess(guess.lower())
        board = hangman.create_board()

        if hangman.has_ended():
            del HANGMAN_DICT[player_id]

        return GameEvent(message, board)
    except KeyError:
        return GameEvent("Hangman game not yet started")

class Hangman:
    def __init__(self, word: str):
        self.__word = word.lower()
        self.__word_mask = self.__create_word_mask(word)
        self.__number_of_wrong_guesses = 0
        self.__max_number_of_wrong_guesses = 10
        self.__solved = False

    @staticmethod
    def __create_word_mask(word: str) -> str:
        return "_" * len(word)

    def do_guess(self, guess: str) -> str:
        if self.__number_of_wrong_guesses >= self.__max_number_of_wrong_guesses: return "You are out of guesses!"
        if self.__solved: return "You have already solved the puzzle!"

        # User tries to guess the entire word
        if len(guess) > 1: return self.__do_word_guess(guess)

        # User tries to guess one of the letters
        return self.__do_letter_guess(guess)

    def __do_word_guess(self, guess) -> str:
        if guess.lower() == self.__word:
            self.__solved = True
            self.__word_mask = self.__word
            return "Congratulations, you have correctly solved the puzzle!"
        else:
            self.__number_of_wrong_guesses += 1
            if self.__number_of_wrong_guesses >= self.__max_number_of_wrong_guesses:
                return f"The word you've guessed is not correct. You're out of guesses, the word is {self.__word}. More luck next time!"
            return "The word you've guessed is not correct"

    def __do_letter_guess(self, guess) -> str:
        if guess not in self.__word:
            self.__number_of_wrong_guesses += 1
            if self.__number_of_wrong_guesses >= self.__max_number_of_wrong_guesses:
                return f"The letter you've guessed is not in the word. You're out of guesses, the word is {self.__word}. More luck next time!"
            return "The letter you've guessed is not in the word"
        else:
            self.__add_letter_to_mask(guess, 0)
            if self.__word == self.__word_mask:
                self.__solved = True
                return "Congratulations, you have correctly solved the puzzle!"
            return f"Correct, the word contains letter {guess}"

    def __add_letter_to_mask(self, letter, start_index) -> None:
        index = self.__word.find(letter, start_index)
        if index == -1: return None
        self.__word_mask = self.__word_mask[:index] + letter + self.__word_mask[index+1:]
        return self.__add_letter_to_mask(letter, index + 1)

    def has_ended(self) -> bool:
        return self.__solved or self.__number_of_wrong_guesses >= self.__max_number_of_wrong_guesses

    def create_board(self) -> str:
        match self.__number_of_wrong_guesses:
            case 0: return " \n \n \n \n \n \n \n \n \n" + self.__word_mask
            case 1: return " \n \n \n \n \n \n \n ___|___\n \n" + self.__word_mask
            case 2: return " \n    |\n    |\n    |\n    |\n    |\n    |\n ___|___\n \n" + self.__word_mask
            case 3: return " ____\n    |\n    |\n    |\n    |\n    |\n    |\n ___|___\n \n" + self.__word_mask
            case 4: return " ____\n |  |\n    |\n    |\n    |\n    |\n    |\n ___|___\n \n" + self.__word_mask
            case 5: return " ____\n |  |\n O  |\n    |\n    |\n    |\n    |\n ___|___\n \n" + self.__word_mask
            case 6: return " ____\n |  |\n O  |\n |  |\n |  |\n    |\n    |\n ___|___\n \n" + self.__word_mask
            case 7: return " ____\n |  |\n O  |\n\\|  |\n |  |\n    |\n    |\n ___|___\n \n" + self.__word_mask
            case 8: return " ____\n |  |\n O  |\n\\|/ |\n |  |\n    |\n    |\n ___|___\n \n" + self.__word_mask
            case 9: return " ____\n |  |\n O  |\n\\|/ |\n |  |\n/   |\n    |\n ___|___\n \n" + self.__word_mask
            case 10: return " ____\n |  |\n O  |\n\\|/ |\n |  |\n/ \\ |\n    |\n ___|___\n \n" + self.__word_mask
        return "Congratulations, you've managed to break the board. I hope you're proud of yourself!"
