import os
from collections import defaultdict


#  Directions to check for adjacent risk levels
DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def load_risk_levels(file_name):
    # Create a list of each digit in the risk levels
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    with open(file_path, "r", encoding="utf-8") as file_risk:
        risk_levels = [
            [int(risk_level) for risk_level in line.strip()] for line in file_risk
        ]

    return risk_levels


def neighbours(position, visited_nodes, nodes_to_visit, risk_levels):
    x, y = position

    for dx, dy in DIRECTIONS:
        if (
            0 <= x + dx <= x_max(risk_levels)
            and 0 <= y + dy <= y_max(risk_levels)
            and (x + dx, y + dy) not in visited_nodes
            and (x + dx, y + dy) not in nodes_to_visit
        ):
            yield (x + dx, y + dy)

    return []


def x_max(risk_levels):
    return len(risk_levels[0]) - 1


def y_max(risk_levels):
    return len(risk_levels) - 1


def find_path_with_lowest_risk(risk_levels):
    destination = (x_max(risk_levels), y_max(risk_levels))

    node_risks = defaultdict(lambda: float("inf"))
    node_risks[(0, 0)] = 0

    nodes_to_visit = []
    visited_nodes = []
    nodes_to_visit.append((0, 0))

    while len(nodes_to_visit) > 0:
        risks_nodes_to_visit = []

        for nodes in nodes_to_visit:
            risks_nodes_to_visit.append(node_risks[nodes])

        current_risk = min(risks_nodes_to_visit)
        x, y = nodes_to_visit[risks_nodes_to_visit.index(current_risk)]

        if (x, y) == destination:
            break

        for neighbour_pos in neighbours(
            (x, y), visited_nodes, nodes_to_visit, risk_levels
        ):
            nodes_to_visit.append(neighbour_pos)
            if (
                current_risk + risk_levels[neighbour_pos[1]][neighbour_pos[0]]
                < node_risks[neighbour_pos]
            ):
                node_risks[neighbour_pos] = (
                    current_risk + risk_levels[neighbour_pos[1]][neighbour_pos[0]]
                )

        visited_nodes.append((x, y))
        nodes_to_visit.remove((x, y))

    return node_risks[destination]


if __name__ == "__main__":
    risk_levels = load_risk_levels("day_15_input.txt")

    lowest_risk = find_path_with_lowest_risk(risk_levels)
    print(lowest_risk)
