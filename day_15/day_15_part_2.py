import os
import heapq as hq


#  Directions to check for adjacent risk levels and colors, to print the path in
DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
COLORS_TURQOISE = "\x1b[38;5;80m"
COLOR_RESET = "\x1b[0m"


def load_risk_levels(file_name):
    # Create a list of each digit in the risk levels
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    with open(file_path, "r", encoding="utf-8") as file_risk:
        risk_levels = [
            [int(risk_level) for risk_level in line.strip()] for line in file_risk
        ]

    return risk_levels


def x_max(risk_entire_cave):
    # Calculate the width of the entire cave
    return len(risk_entire_cave[0]) - 1


def y_max(risk_entire_cave):
    # Calculate the length of the entire cave
    return len(risk_entire_cave) - 1


def create_5x5_tile_cave(risk_levels):
    # Create the entire cave which is made of the given tile and appended 5
    # times in both dimensions. Every time the tile is appended in one of the
    # directions, the risk levels are raised by one. If they reach a value
    # greater than 9, they are set to one.
    x_max_tile = x_max(risk_levels) + 1
    y_max_tile = y_max(risk_levels) + 1
    entire_cave = [[] for y in range(y_max_tile * 5)]

    for y in range(y_max_tile * 5):
        for x in range(x_max_tile * 5):
            entire_cave[y].append(
                (
                    risk_levels[y % y_max_tile][x % x_max_tile]
                    + int(x / x_max_tile)
                    + int(y / y_max_tile)
                    - 1
                )
                % 9
                + 1
            )

    return entire_cave


def neighbors(position, x_max_cave, y_max_cave):
    # Check, if neighbors in the given directions exist and return their positions
    x, y = position

    for dx, dy in DIRECTIONS:
        if 0 <= x + dx <= x_max_cave and 0 <= y + dy <= y_max_cave:
            yield (x + dx, y + dy)

    return []


def find_path_with_lowest_risk(risk_entire_cave):
    # Finding the path with the lowest risk using the Dijkstra algorithm. First,
    # the destination and the starting point are defined. Starting from the top
    # left corner, the risks of the neighboring nodes are calculated and are
    # added to the heap nodes_to_visit together with the position of the current
    # node as well as the path with the lowest risk, that leads to it. To track,
    # which nodes have already been visited, a set of all nodes is created
    # (unvisited_nodes). If the current node is not in this set, the node is
    # checked for neighbors and their new risks as well as the path to them are
    # stored in the heap (nodes_to_visit). The current node is then removed from
    # the set of unvisited_nodes. Nodes, that have been added more than once to
    # the heap or even have the wrong current risk, which might happen because
    # it was later updated to a lower value, are intercepted, because after the
    # first check, the node is removed from the set of unvisted_nodes. From all
    # duplicates or all nodes with false risks, only the one with the lowest risk
    # is checked, since a heap is used. If the destination has been reached, the
    # while loop breaks and the path to the destination as well as its risk are
    # returned.
    x_max_cave = x_max(risk_entire_cave)
    y_max_cave = y_max(risk_entire_cave)
    destination = (x_max_cave, y_max_cave)

    nodes_to_visit = []
    path = [(0, 0)]
    hq.heappush(nodes_to_visit, (0, (0, 0), path))

    unvisited_nodes = set()
    for y, line in enumerate(risk_entire_cave):
        for x, risk_level in enumerate(line):
            unvisited_nodes.add((x, y))

    while len(nodes_to_visit) > 0:
        # Because of performance reasons, the while loop checks, if there are
        # still elements in nodes_to_visit, insted of checking if the destination
        # node is still in the set of unvisited_nodes.
        current_risk, current_node, path = hq.heappop(nodes_to_visit)

        if current_node not in unvisited_nodes:
            continue

        if current_node == destination:
            break

        for neighbor_node in neighbors(current_node, x_max_cave, y_max_cave):
            if neighbor_node not in unvisited_nodes:
                continue

            neighbor_risk = (
                current_risk + risk_entire_cave[neighbor_node[1]][neighbor_node[0]]
            )
            hq.heappush(
                nodes_to_visit,
                (neighbor_risk, neighbor_node, list(path) + [neighbor_node]),
            )

        unvisited_nodes.remove(current_node)

    return current_risk, path


def visualize_path(risk_entire_cave, path) -> str:
    # Visualize the path with the lowest risk
    x_max_cave = x_max(risk_entire_cave)
    y_max_cave = y_max(risk_entire_cave)
    text = ""

    for y in range(y_max_cave):
        for x in range(x_max_cave):
            if (x, y) in path:
                text = f"{text}{COLORS_TURQOISE}{risk_entire_cave[y][x]}{COLOR_RESET}"
            else:
                text = f"{text}{risk_entire_cave[y][x]}"

        text = f"{text}\n"

    return text


if __name__ == "__main__":
    risk_entire_cave = create_5x5_tile_cave(load_risk_levels("day_15_input.txt"))

    lowest_risk, path = find_path_with_lowest_risk(risk_entire_cave)

    print(
        "\n".join(str(node) for node in path),
        f"\nThe lowest risk of all paths is: {lowest_risk}",
        # "\nPath:\n" + visualize_path(risk_entire_cave, path),
    )
