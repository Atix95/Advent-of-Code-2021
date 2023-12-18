import os
import re
import math


def load_input(file_name: str) -> dict[int, list[list[int, int, int]]]:
    input = {}

    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))

    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        if line.startswith("--- scanner"):
            scanner_number = int(re.findall(r"\d+", line)[0])
            input[scanner_number] = []
        elif line != "":
            input[scanner_number].append([int(number) for number in line.split(",")])

    return input


class Scanner:
    def __init__(self, scanner_number: int, readings: list[list[int, int, int]]):
        self.scanner_number = scanner_number
        self.readings = readings
        self.beacon_spacings = self.distances_between_beacons()
        self.neighbours = []
        self.number_of_non_overlapping_beacons = len(readings)

    def __repr__(self):
        output = ""
        output += f"Scanner {self.scanner_number}:\n"
        for reading in self.readings:
            output += f"{reading}\n"
        return output

    def get_readings(self) -> list[list[int, int, int]]:
        return self.readings

    def get_scanner_number(self) -> int:
        return self.scanner_number

    def distances_between_beacons(self) -> list[float]:
        beacons = self.readings.copy()
        distances = []
        for _ in range(len(beacons) - 1):
            x_1, y_1, z_1 = beacons.pop(0)

            for beacon in beacons:
                x_2, y_2, z_2 = beacon
                distance = math.sqrt(
                    (x_1 - x_2) ** 2 + (y_1 - y_2) ** 2 + (z_1 - z_2) ** 2
                )
                distances.append(distance)

        return distances


def number_of_overlapping_beacons_from_distances(
    number_of_overlapping_distances_between_scanners: int,
) -> int:
    """
    The number of overlapping distances between scanners is given by 1 + the sum over k
    with the limit n, which is also the number of overlapping beacons. The result of
    this sum is  n(n+1)/2. Rearranging this equation to solve for n gives the following
    equation (Here, only the positive solution is of interest).
    """
    return (
        round(
            -1 / 2
            + math.sqrt(1 / 4 + 2 * number_of_overlapping_distances_between_scanners)
        )
        + 1
    )


def find_neighbours(scanners: list[Scanner]) -> None:
    for scanner in scanners:
        remaining_scanners = scanners[scanner.scanner_number + 1 :]

        for remaining_scanner in remaining_scanners:
            number_of_overlapping_distances_between_scanners = 0
            for distance in scanner.beacon_spacings:
                for other_distance in remaining_scanner.beacon_spacings:
                    if math.isclose(distance, other_distance):
                        number_of_overlapping_distances_between_scanners += 1

            number_of_overlapping_beacons = (
                number_of_overlapping_beacons_from_distances(
                    number_of_overlapping_distances_between_scanners
                )
            )
            if number_of_overlapping_beacons >= 12:
                scanner.neighbours.append(
                    (
                        remaining_scanner.get_scanner_number(),
                        number_of_overlapping_beacons,
                    )
                )
                remaining_scanner.neighbours.append(
                    (scanner.get_scanner_number(), number_of_overlapping_beacons)
                )
                scanner.number_of_non_overlapping_beacons -= (
                    number_of_overlapping_beacons
                )

    return scanners


def number_of_beacons(scanners: list[Scanner]) -> int:
    number_of_beacons = 0

    for scanner in scanners:
        number_of_beacons += scanner.number_of_non_overlapping_beacons

    return number_of_beacons


if __name__ == "__main__":
    scanners = []
    input = load_input("day_19_example_input.txt")

    for scanner_number in input.keys():
        scanners.append(Scanner(scanner_number, input[scanner_number]))

    scanners = find_neighbours(scanners)
    print(number_of_beacons(scanners))
