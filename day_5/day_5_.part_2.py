from dataclasses import replace
import os

example_lines = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "day_5_input.txt")
with open(file_path, "r", encoding="utf-8") as file_lines:
    lines = [line for line in file_lines.read().strip().split("\n")]


def create_position_tuple(lines):
    grid_size = 0

    for line in range(len(lines)):
        lines[line] = lines[line].split(" -> ")
        x_1, y_1 = lines[line][0].split(",")
        lines[line][0] = (int(x_1), int(y_1))
        x_2, y_2 = lines[line][1].split(",")
        lines[line][1] = (int(x_2), int(y_2))
        grid_size = max(grid_size, int(x_1), int(x_2), int(y_1), int(y_2))

    return lines, grid_size


def diagonal_and_straight_lines(lines, grid_size):
    diagram = [[0 for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]
    overlap = 0

    for line in range(len(lines)):
        x_1 = lines[line][0][0]
        y_1 = lines[line][0][1]
        x_2 = lines[line][1][0]
        y_2 = lines[line][1][1]
        if x_1 == x_2:
            if y_2 > y_1:
                for length in range(abs(y_2 - y_1) + 1):
                    diagram[y_1 + length][x_1] += 1
            else:
                for length in range(abs(y_2 - y_1) + 1):
                    diagram[y_1 - length][x_1] += 1
        elif y_1 == y_2:
            if x_2 > x_1:
                for length in range(abs(x_2 - x_1) + 1):
                    diagram[y_1][x_1 + length] += 1
            else:
                for length in range(abs(x_2 - x_1) + 1):
                    diagram[y_1][x_1 - length] += 1
        elif x_2 > x_1:
            if y_2 > y_1:
                for length in range(abs(x_2 - x_1) + 1):
                    diagram[y_1 + length][x_1 + length] += 1
            else:
                for length in range(abs(x_2 - x_1) + 1):
                    diagram[y_1 - length][x_1 + length] += 1
        elif x_1 > x_2:
            if y_2 > y_1:
                for length in range(abs(x_2 - x_1) + 1):
                    diagram[y_1 + length][x_1 - length] += 1
            else:
                for length in range(abs(x_2 - x_1) + 1):
                    diagram[y_1 - length][x_1 - length] += 1

    for line in diagram:
        for colum in line:
            if colum > 1:
                overlap += 1

    return diagram, overlap


lines, grid_size = create_position_tuple(lines)
diagram, overlap = diagonal_and_straight_lines(lines, grid_size)

for line in range(grid_size + 1):
    print(diagram[line])

print(f"The number of overlaping points is: {overlap}")
