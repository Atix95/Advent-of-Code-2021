from pathlib import Path
import numpy as np


example_draws = [
    7, 4, 9,
    5, 11, 17,
    23, 2, 0,
    14, 21, 24,
    10, 16, 13,
    6, 15, 25,
    12, 22, 18,
    20, 8, 19,
    3, 26, 1
]

example_boards = [
        [22, 13, 17, 11, 0],
        [8, 2, 23,  4, 24],
        [21, 9, 14, 16, 7],
        [6, 10, 3, 18, 5],
        [1, 12, 20, 15, 19],
        [3, 15, 0, 2, 22],
        [9, 18, 13, 17, 5],
        [19, 8, 7, 25, 23],
        [20, 11, 10, 24, 4],
        [14, 21, 16, 12, 6],
        [14, 21, 17, 24, 4],
        [10, 16, 15, 9, 19],
        [18, 8, 23, 26, 20],
        [22, 11, 13, 6, 5],
        [2, 0, 12, 3, 7]
]

p = Path(__file__).with_name('day_4_input.txt')

with p.open('r', encoding='utf-8') as file_draw:
    draws = [int(x) for x in file_draw.readlines().pop(0).split(',')]
with p.open('r', encoding='utf-8') as file_boards:
    boards = np.loadtxt(file_boards, skiprows=1).tolist()


def bingo_board_last(board, draw):
    marked_numbers = [ [] for _ in range(int(len(board)/5))]
    score = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(int(len(board)/5))]
    sum_unmarked_numbers = 0
    winner_order = []

    for i in range(len(draw)):
        for j in range(len(board)):
            try:
                column = board[j].index(draw[i])
                row = j%5
                board_number = int(j/5)
                marked_numbers[board_number].append((row, column))
                score[board_number][column] += 1
                score[board_number][row+5] += 1
                score[board_number].index(5)
                if board_number not in winner_order:
                    winner_order.append(board_number)
            except ValueError:
                pass
        if int(len(board)/5) == len(winner_order):
            last_draw = draw[i]
            break

    for k in range(5):
        sum_unmarked_numbers += sum(board[winner_order[-1]*5 + k])
    for l in range(len(marked_numbers[winner_order[-1]])):
        position = marked_numbers[winner_order[-1]][l]
        sum_unmarked_numbers -= board[winner_order[-1]*5 + position[0]][position[1]]

    print(f'Board No. {winner_order[-1]+1} wins last!')
    print(f'The final score of Board {winner_order[-1]+1} is: {int(sum_unmarked_numbers*last_draw)}.')


bingo_board_last(boards, draws)
