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


def find_path_with_lowest_risk(risk_levels):
    x_max = len(risk_levels[0]) - 1
    y_max = len(risk_levels) - 1
    destination = (x_max, y_max)

    node_risks = defaultdict(lambda: float("inf"))
    node_risks[(0, 0)] = 0

    nodes_to_visit = []
    visited_notes = []
    nodes_to_visit.append((0, 0))

    while len(nodes_to_visit) > 0:
        risks_nodes_to_visit = []

        for nodes in nodes_to_visit:
            risks_nodes_to_visit.append(node_risks[nodes])

        current_risk = min(risks_nodes_to_visit)
        current_node = nodes_to_visit[risks_nodes_to_visit.index(current_risk)]
        x, y = current_node

        for dx, dy in DIRECTIONS:
            if (
                0 <= x + dx <= x_max
                and 0 <= y + dy <= y_max
                and (x + dx, y + dy) not in visited_notes
            ):
                nodes_to_visit.append((x + dx, y + dy))
                if (
                    current_risk + risk_levels[y + dy][x + dx]
                    < node_risks[(x + dx, y + dy)]
                ):
                    node_risks[(x + dx, y + dy)] = (
                        current_risk + risk_levels[y + dy][x + dx]
                    )

        visited_notes.append((x, y))
        nodes_to_visit.remove((x, y))

    return node_risks[destination]


if __name__ == "__main__":
    risk_levels = load_risk_levels("day_15_example_input.txt")
    for line in risk_levels:
        print(line)

    lowest_risk = find_path_with_lowest_risk(risk_levels)
    print(lowest_risk)
