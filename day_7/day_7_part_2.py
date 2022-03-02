import os


def load_crab_positions(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_crabs:
        crab_positions = [
            int(crab_position) for crab_position in file_crabs.read().strip().split(",")
        ]

    return crab_positions


def count_initial_positions(crab_positions):
    counted_positions = []

    for positions in range(max(crab_positions) + 1):
        # Create a list of the quantitiy of each position
        # The 0 element in the list is the number of crabs in position 0
        # The 1 element in the list is the number of crabs in position 1 etc.
        counted_positions.append(crab_positions.count(positions))

    return counted_positions


def find_cheapest_possible_outcome(counted_positions):
    fuel_per_position = [0 for positions in range(len(counted_positions))]

    for possible_position in range(len(counted_positions)):
        for position, quantity in enumerate(counted_positions):
            # Calculate fuel cost for each possible position
            fuel_per_position[possible_position] += (
                abs(position - possible_position)
                * (abs(position - possible_position) + 1)
                // 2
                * quantity
            )

    return fuel_per_position


if __name__ == "__main__":
    fuel_per_position = find_cheapest_possible_outcome(
        count_initial_positions(load_crab_positions("day_7_input.txt"))
    )

    print(
        f"The position that costs the least fuel is poition {fuel_per_position.index(min(fuel_per_position))}"
        + f" with a fuel cost of: {min(fuel_per_position)}"
    )
