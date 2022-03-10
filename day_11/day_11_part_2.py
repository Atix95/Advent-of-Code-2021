import os


# Directions to check for adjacent octopuses of a flashing octopus
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]


def load_energy_level(file_name):
    # Create a list of each digit in the energy levels
    split_num_into_digits = lambda num: [int(digit) for digit in str(num)]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_energy_levels:
        energy_levels = [
            split_num_into_digits(line) for line in file_energy_levels.read().split("\n")
        ]

    return energy_levels


def octopus_flashes(energy_levels):
    # Track the steps till all octopuses flash
    steps_till_synchronization = 0

    # List of tuples containing the indices of flashing octopuses per step, that have not yet
    # been checked for adjacent octopuses. The unchecked flashing octopuses are stored in a
    # second list and are removed from the first list, after being checked for adjacent octopuses.
    unchecked_flashing_octopuses = []
    checked_flashing_octopuses = []

    # Number of octopuses in x and y direction as well as the number of all octopuses
    width = len(energy_levels[0])  # In octopuses
    height = len(energy_levels)  # In octopuses
    num_of_octopuses = width * height  # In octopuses square ;)
    # bla
    while len(checked_flashing_octopuses) < num_of_octopuses:
        # Reset the list of checked and unchecked octopuses
        unchecked_flashing_octopuses = []
        checked_flashing_octopuses = []

        for y, line in enumerate(energy_levels):
            for x in range(len(line)):
                # Increase all energy levels by 1 and check if they are greater than 9.
                # If so add it to the list of unchecked flashing octopuses.
                energy_levels[y][x] += 1
                if energy_levels[y][x] > 9:
                    unchecked_flashing_octopuses.append((x, y))

        while len(unchecked_flashing_octopuses) > 0:
            # Increase the energy levels of all adjacent octopuses to the previously found
            # flashing octopuses. If the energy level is greater than 9 and the flashing
            # octopus is not yet in the list of checked octopuses, add it to said list.
            # Then remove the octopus from the list of unchecked octopuses.
            x = unchecked_flashing_octopuses[0][0]
            y = unchecked_flashing_octopuses[0][1]

            for dx, dy in DIRECTIONS:
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    energy_levels[y + dy][x + dx] += 1
                    if (
                        energy_levels[y + dy][x + dx] > 9
                        and (x + dx, y + dy) not in checked_flashing_octopuses
                        and (x + dx, y + dy) not in unchecked_flashing_octopuses
                    ):
                        unchecked_flashing_octopuses.append((x + dx, y + dy))

            checked_flashing_octopuses.append((x, y))
            unchecked_flashing_octopuses = unchecked_flashing_octopuses[1:]

        for x, y in checked_flashing_octopuses:
            # Reset the energy level of all flashing octopuses to 0
            energy_levels[y][x] = 0

        steps_till_synchronization += 1

    return steps_till_synchronization


if __name__ == "__main__":
    steps_till_synchronization = octopus_flashes(load_energy_level("day_11_input.txt"))

    print(
        f"The number of steps till all octopuses flash is: {steps_till_synchronization}"
    )
