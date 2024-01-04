import itertools
import os


class Player:
    def __init__(self, number: int, position: int, score: int = 0) -> None:
        self.number = number
        self.position = position
        self.score = score

    def __str__(self) -> str:
        return (
            f"Player {self.number} is at position {self.position} with score "
            + f"{self.score}."
        )


class DiracDice:
    def __init__(self) -> None:
        """
        Class that represents the Dirac dice game. It can play a practice game and a
        real game. The practice game is played with deterministic dice, i.e., the dice
        always rolls a the next number in the sequence from 1 to 100. The real game is
        played with a quantum die, i.e., the dice rolls a number from 1 to 3 and creates
        a superposition of the three possible outcomes. The game is deterministic, i.e.,
        the same game state can be reached multiple times, as the game state is defined
        by the 10 player positions and the 21 player scores yielding 10*10*21*21=44100
        different game states.

        Attributes:
            board : list[int]
                The circular board of the game with positions from 1 to 10.

            deterministic_dice : list[int]
                The deterministic dice with numbers from 1 to 100.

            dice_position : int
                The current position of the deterministic dice.

            players : list[Player]
                The players of the game that are initialized with their number and
                position using the Player class.

            quantum_die : list[int]
                The quantum die with numbers from 1 to 3.

            cache : dict[tuple[int, int, int, int], tuple[int, int]]
                Dictionary that caches the scores of the players for a given game state.
                The game state is defined by the scores of the two players and their
                positions.
        """
        self.board = [count + 1 for count in range(10)]
        self.deterministic_dice = [count + 1 for count in range(100)]
        self.dice_position = 1
        self.players = []
        self.quantum_die = [1, 2, 3]
        self.cache = {}

    def __str__(self) -> str:
        output = ""
        for player in self.players:
            output += f"{player}\n"
        return output

    def initialize_players(self, file_name: str) -> None:
        """Initialize the players with their number and position."""
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
        with open(file_path, "r") as file:
            self.players = [
                Player(int(line.split()[1]), int(line.split()[-1]))
                for line in file.readlines()
            ]

    def moves(self, player: Player, dice_throws: int, moves: int) -> int:
        """
        Recursive function to calculate the moves of a player. When the dice position
        exceeds the length of the deterministic dice, the dice position is reset to 1.
        """
        dice_throws -= 1
        moves += self.deterministic_dice[self.dice_position - 1]

        self.dice_position += 1
        if self.dice_position == 101:
            self.dice_position = 1

        if dice_throws == 0:
            return moves

        return self.moves(player, dice_throws, moves)

    def players_take_practice_turns(
        self, num_of_dice_rolls, board_length: int, dice_length: int
    ) -> int:
        """
        Recursive function to let the players take turns. If a player reaches a position
        of zero, i.e., the end of a board, the position is set to the length of the
        board. When a player reaches a score of 1000 the game immeadiately ends.
        """
        for player in self.players:
            moves = self.moves(player, 3, 0)
            num_of_dice_rolls += 3

            player.position = (player.position + moves) % board_length
            if player.position == 0:
                player.position = board_length
            player.score += self.board[player.position - 1]

            if player.score >= 1000:
                return num_of_dice_rolls

        return self.players_take_practice_turns(
            num_of_dice_rolls, board_length, dice_length
        )

    def play_practice_game(self, file_name: str):
        self.initialize_players(file_name)
        board_length = len(self.board)
        dice_length = len(self.deterministic_dice)
        num_of_dice_rolls = 0

        num_of_dice_rolls = self.players_take_practice_turns(
            num_of_dice_rolls, board_length, dice_length
        )

        self.announce_winner_of_practice_game(num_of_dice_rolls)

    def announce_winner_of_practice_game(self, num_of_dice_rolls) -> int:
        scores = sorted([(player.score, player.number) for player in self.players])
        print(
            "Practice game:\n"
            + f"The dice has been rolled {num_of_dice_rolls} times.\n{self}"
            + f"Player {scores[-1][-1]} has won the practice game.\n"
            + f"The final score is: {scores[-2][0]*num_of_dice_rolls}"
        )

    def take_turns(
        self,
        current_player_score: int,
        waiting_player_score: int,
        current_player_position: int,
        waiting_player_position: int,
        board_length: int,
    ) -> tuple[int, int]:
        """
        Many thanks to TrickWasabi4 on reddit for the explanation of the dynamic
        solution. My loop solution was very very slow...

        Dynamic solution explanation:
        The state of the game is defined by the scores of the two players and their
        positions. Creating a new player object for each game state, i.e., each time a
        new position (or rather a new universe) is reached, results in a new object that
        cannot be used for caching in the dictionary as the hash value of the object
        changes. Since the hash value of a tuple containing integers does not change,
        the scores and positions are parsed to take_turns(). All possibles rolls for
        the current player are considered and the scores and positions are updated
        accordingly. Note that new variables "new_position" and "new_score" must be
        created, because the original variables are used for the recursive calls. After
        the recursive call, the total score between the players is updated. As soons as
        all possible rolls have been considered for the current player, the total score
        is cached in a dictionary. If the same game state is reached again, the cached
        score is returned. This is possible, because the game is deterministic and the
        same game state can be reached again, since each player can have 10 different
        positions and 21 different scores yielding 10*10*21*21 = 44100 different game
        states.
        """
        if current_player_score >= 21:
            return 1, 0
        if waiting_player_score >= 21:
            return 0, 1
        if (
            current_player_score,
            waiting_player_score,
            current_player_position,
            waiting_player_position,
        ) in self.cache:
            return self.cache[
                (
                    current_player_score,
                    waiting_player_score,
                    current_player_position,
                    waiting_player_position,
                )
            ]

        score = (0, 0)
        for roll_1, roll_2, roll_3 in itertools.product(self.quantum_die, repeat=3):
            moves = roll_1 + roll_2 + roll_3
            new_position = (current_player_position + moves) % board_length
            if new_position == 0:
                new_position = board_length

            new_score = current_player_score + self.board[new_position - 1]

            player_2_wins, player_1_wins = self.take_turns(
                waiting_player_score,
                new_score,
                waiting_player_position,
                new_position,
                board_length,
            )
            score = (score[0] + player_1_wins, score[1] + player_2_wins)

        self.cache[
            (
                current_player_score,
                waiting_player_score,
                current_player_position,
                waiting_player_position,
            )
        ] = score
        return score

    def play_game(self, file_name: str):
        self.initialize_players(file_name)
        board_length = len(self.board)
        player_1, player_2 = self.players

        score = self.take_turns(
            player_1.score,
            player_2.score,
            player_1.position,
            player_2.position,
            board_length,
        )
        self.announce_winner_of_the_game(score)

    def announce_winner_of_the_game(self, score: tuple[int, int]) -> None:
        if score[0] > score[1]:
            print(f"Player 1 has won the game with a score of: {score[0]}")
        elif score[0] < score[1]:
            print(f"Player 2 has won the game with a score of: {score[1]}")
        else:
            print("The game ended in a draw.")


if __name__ == "__main__":
    dirac_dice = DiracDice()
    dirac_dice.play_practice_game("day_21_input.txt")
    dirac_dice.play_game("day_21_input.txt")
