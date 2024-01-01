import itertools
import math
import os
import re
from collections import defaultdict


def load_input(file_name: str) -> dict[int, list[list[int, int, int]]]:
    """
    Load the intput from the file and return a dictionary with the scanner number as
    key and a list of the readings as value.
    """
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
        self.number = scanner_number
        self.readings = readings
        self.position = None
        self.rotation = None
        self.beacon_spacings = self.calculate_beacon_spacings()
        self.neighbours = {}
        self.link_to_reference_scanner = []

    def __repr__(self):
        """
        Representing the scanner in the same way as the input is given.
        """
        output = ""
        output += f"Scanner {self.number}:\n"
        for reading in self.readings:
            output += f"{reading}\n"
        return output

    def get_readings(self) -> list[list[int, int, int]]:
        """
        Readings are given as a list of list with the x, y and z coordinates of the
        beacon.
        """
        return self.readings

    def get_number(self) -> int:
        """
        The number of the scanner from the input file.
        """
        return self.number

    def get_position(self) -> list[int, int, int]:
        """
        The position of the scanner compared to the reference scanner.
        """
        return self.position

    def get_rotation(self) -> int:
        """
        The rotation of the scanner compared to the reference scanner.
        """
        return self.rotation

    def get_beacon_spacings(
        self,
    ) -> list[list[float, list[int, int, int], list[int, int, int]]]:
        """
        The distance between two beacons is given by the euclidean distance between the
        two beacons. The list contains the distance between the two beacons and the
        coordinates of the two beacons.
        """
        return self.beacon_spacings

    def get_neighbours(self) -> dict[int, list[list[int, int, int]]]:
        """
        The neighbours of the scanner are given by a dictionary with the scanner number
        as key and a list of the overlapping beacons, which are given as list of the x,
        y and z value, as value.
        """
        return self.neighbours

    def get_link_to_reference_scanner(self) -> list[int]:
        """
        The link to the reference scanner is given by a list of the scanner numbers
        which are connected to the reference scanner.
        """
        return self.link_to_reference_scanner

    def calculate_beacon_spacings(
        self,
    ) -> list[list[float, list[int, int, int], list[int, int, int]]]:
        """
        Euclidean distance between two beacons is given by the following equation:
        sqrt((x_1 - x_2)^2 + (y_1 - y_2)^2 + (z_1 - z_2)^2)
        """
        beacons = self.readings.copy()
        distances = []
        for _ in range(len(beacons) - 1):
            x_1, y_1, z_1 = beacons.pop(0)

            for beacon in beacons:
                x_2, y_2, z_2 = beacon
                distance = math.sqrt(
                    (x_1 - x_2) ** 2 + (y_1 - y_2) ** 2 + (z_1 - z_2) ** 2
                )
                distances.append([distance, [x_1, y_1, z_1], [x_2, y_2, z_2]])

        return distances


def number_of_overlapping_beacons(
    number_of_overlapping_distances_between_scanners: int,
) -> int:
    """
    The number of overlapping distances between scanners is given by 1 + the sum over k
    with the limit n, where n is the number of overlapping beacons. The result of
    this sum is n(n+1)/2. Rearranging this equation to solve for n gives the following
    equation (Here, only the positive solution is of interest):
    """
    return (
        round(
            -1 / 2
            + math.sqrt(1 / 4 + 2 * number_of_overlapping_distances_between_scanners)
        )
        + 1
    )


def find_neighbours(scanners: list[Scanner]) -> list[list[int, int, int]]:
    """
    Find the neighbours of each scanner. Two scanners are neighbours if they have at
    least 12 overlapping beacons. The number of overlapping beacons is determined from
    the number of overlapping distances between two scanners using
    number_of_overlapping_beacons(). The overlapping beacons are stored in a dictionary
    with the scanner number as key and a list of the overlapping beacons as value and
    parsed to the neighbours attribute of the scanner.
    """
    for scanner in scanners:
        remaining_scanners = scanners[scanner.get_number() + 1 :]

        for remaining_scanner in remaining_scanners:
            beacons = []
            other_beacons = []
            overlapping_distances = 0
            for distance, beacon_1, beacon_2 in scanner.get_beacon_spacings():
                for (
                    other_distance,
                    other_beacon_1,
                    other_beacon_2,
                ) in remaining_scanner.get_beacon_spacings():
                    if math.isclose(distance, other_distance):
                        overlapping_distances += 1
                        if beacon_1 not in beacons:
                            beacons.append(beacon_1)
                        if beacon_2 not in beacons:
                            beacons.append(beacon_2)
                        if other_beacon_1 not in other_beacons:
                            other_beacons.append(other_beacon_1)
                        if other_beacon_2 not in other_beacons:
                            other_beacons.append(other_beacon_2)

            if number_of_overlapping_beacons(overlapping_distances) >= 12:
                scanner.get_neighbours()[remaining_scanner.get_number()] = []
                remaining_scanner.get_neighbours()[scanner.get_number()] = []

                for beacon, other_beacon in zip(beacons, other_beacons):
                    scanner.get_neighbours()[remaining_scanner.get_number()].append(
                        beacon
                    )
                    remaining_scanner.get_neighbours()[scanner.get_number()].append(
                        other_beacon
                    )


def rotate_coordinates(
    beacon: list[int, int, int], rotation: int
) -> list[int, int, int]:
    """
    In total there are 6 permutations of a set of coordinates [x, y, z]. Flipping the
    axis of the coordinate system is equivalent to changing the sign of one of the three
    axis. Counting the number of permutations with a negative sign yields 48 different
    permutations in total.
    """
    assert rotation in range(48)

    permutation = [list(permutation) for permutation in itertools.permutations(beacon)][
        rotation // 8
    ]

    if rotation % 2 == 1:
        permutation[0] *= -1
    if (rotation // 2) % 2 == 1:
        permutation[1] *= -1
    if (rotation // 4) % 2 == 1:
        permutation[2] *= -1

    return permutation


def rotate_scanner(
    scanners: list[Scanner],
    coordinates: list[int, int, int],
    list_of_scanners_to_rotate_to: list[int],
) -> list[int, int, int]:
    """
    Recursive function to rotate the scanner to the reference scanner. The function
    rotates a set of coordinates to the reference scanner. The list of scanners to
    rotate to contains the scanner numbers of the scanners which are connected to the
    reference scanner. The function is called recursively until the list of scanners to
    rotate to is empty.
    """
    if not list_of_scanners_to_rotate_to:
        return coordinates

    scanner_number = list_of_scanners_to_rotate_to.pop()
    coordinates = rotate_coordinates(
        coordinates, scanners[scanner_number].get_rotation()
    )
    return rotate_scanner(scanners, coordinates, list_of_scanners_to_rotate_to)


def set_reference_scanner(
    scanners: list[Scanner], reference_scanner_number: int
) -> list[Scanner]:
    """
    Set the reference scanner to the scanner with the given scanner number. The
    reference scanner is the scanner which is used as reference for the position of the
    other scanners. The reference scanner is set to the position [0, 0, 0] and the
    rotation 0. The link to reference scanner is set to the scanner number.
    """
    reference_scanner = scanners[reference_scanner_number]
    reference_scanner.position = [0, 0, 0]
    reference_scanner.rotation = 0
    reference_scanner.link_to_reference_scanner.append(reference_scanner_number)

    return reference_scanner


def find_all_beacons(scanners: list[Scanner], reference_scanner_number: int = 0):
    """
    Find all beacons by rotating the neighbouring scanners to the reference scanner.
    The function starts with the reference scanner and rotates the neighbouring scanners
    to the reference scanner. The position of a scanner is determined from the
    overlapping beacons between the neighbouring scanner and the current scanner by
    rotating the overlapping beacons and determining the position for each rotation. The
    correct position is found when the same position is calculated at least 12 times,
    which is tracked by the dictionary counter. Then, the position of the neighbour is
    determined compared to the reference scanner by rotating the position recursively
    to the reference scanner. This is done by tracking the link to the reference scanner
    with the attribute link_to_reference_scanner. Lastly, the beacons of the neighbour
    are rotated and translated to the reference scanner and added to the list of all
    beacons.
    """
    all_beacons_compared_to_reference_scanner = []

    reference_scanner = set_reference_scanner(scanners, reference_scanner_number)

    for beacon in reference_scanner.get_readings():
        all_beacons_compared_to_reference_scanner.append(beacon)

    scanners_to_rotate = [reference_scanner.get_number()]
    checked_scanners = set()

    while scanners_to_rotate:
        scanner_number = scanners_to_rotate.pop(0)
        scanner_position_found = False

        for neighbour_number, overlapping_beacons in (
            scanners[scanner_number].get_neighbours().items()
        ):
            if (
                scanner_number in checked_scanners
                and neighbour_number in checked_scanners
            ):
                continue

            scanners_to_rotate.append(neighbour_number)
            scanners[neighbour_number].link_to_reference_scanner = (
                scanners[scanner_number].get_link_to_reference_scanner().copy()
            )
            scanners[neighbour_number].link_to_reference_scanner.append(
                neighbour_number
            )

            counter = defaultdict(int)
            for overlapping_beacon in overlapping_beacons:
                for neighbouring_beacon in scanners[neighbour_number].get_neighbours()[
                    scanner_number
                ]:
                    for rotation in range(48):
                        rotated_beacon = rotate_coordinates(
                            neighbouring_beacon, rotation
                        )

                        position_x = overlapping_beacon[0] - rotated_beacon[0]
                        position_y = overlapping_beacon[1] - rotated_beacon[1]
                        position_z = overlapping_beacon[2] - rotated_beacon[2]

                        counter[(position_x, position_y, position_z, rotation)] += 1

            for (
                position_x,
                position_y,
                position_z,
                rotation,
            ), value in counter.items():
                if value >= 12:
                    scanner_position_found = True

                    if scanners[neighbour_number].get_rotation() is None:
                        scanners[neighbour_number].rotation = rotation

                    if scanners[neighbour_number].get_position() is None:
                        rotate_position_to_matching_scanner = rotate_scanner(
                            scanners,
                            [position_x, position_y, position_z],
                            scanners[neighbour_number]
                            .get_link_to_reference_scanner()
                            .copy()[:-1],
                        )
                        scanners[neighbour_number].position = [
                            scanners[scanner_number].get_position()[0]
                            + rotate_position_to_matching_scanner[0],
                            scanners[scanner_number].get_position()[1]
                            + rotate_position_to_matching_scanner[1],
                            scanners[scanner_number].get_position()[2]
                            + rotate_position_to_matching_scanner[2],
                        ]

                    for beacon in scanners[neighbour_number].get_readings():
                        rotated_neighbouring_beacon = rotate_scanner(
                            scanners,
                            beacon,
                            scanners[neighbour_number]
                            .get_link_to_reference_scanner()
                            .copy(),
                        )
                        translated_beacon = [
                            rotated_neighbouring_beacon[0]
                            + scanners[neighbour_number].get_position()[0],
                            rotated_neighbouring_beacon[1]
                            + scanners[neighbour_number].get_position()[1],
                            rotated_neighbouring_beacon[2]
                            + scanners[neighbour_number].get_position()[2],
                        ]
                        if (
                            translated_beacon
                            not in all_beacons_compared_to_reference_scanner
                        ):
                            all_beacons_compared_to_reference_scanner.append(
                                translated_beacon
                            )
                    break

            if not scanner_position_found:
                raise ValueError(
                    f"The position of scanner {scanner_number} could not be found."
                )

            checked_scanners.add(scanner_number)
            checked_scanners.add(neighbour_number)

    return all_beacons_compared_to_reference_scanner


def largest_manhattan_distance_between_scanners(scanners: list[Scanner]) -> int:
    manhatten_distances_between_scanners = []

    for scanner in scanners:
        remaining_scanners = scanners[scanner.get_number() + 1 :]

        for remaining_scanner in remaining_scanners:
            manhatten_distance = (
                abs(
                    scanners[scanner.get_number()].get_position()[0]
                    - scanners[remaining_scanner.get_number()].get_position()[0]
                )
                + abs(
                    scanners[scanner.get_number()].get_position()[1]
                    - scanners[remaining_scanner.get_number()].get_position()[1]
                )
                + abs(
                    scanners[scanner.get_number()].get_position()[2]
                    - scanners[remaining_scanner.get_number()].get_position()[2]
                )
            )
            manhatten_distances_between_scanners.append(manhatten_distance)

    return max(manhatten_distances_between_scanners)


def main() -> None:
    scanners = []
    input = load_input("day_19_input.txt")

    for scanner_number in input.keys():
        scanners.append(Scanner(scanner_number, input[scanner_number]))

    find_neighbours(scanners)
    all_beacons_compared_to_reference_scanner = find_all_beacons(scanners)

    print(f"The number of beacons is: {len(all_beacons_compared_to_reference_scanner)}")
    print(
        f"The largest Manhatten distance between scanners is: "
        + f"{largest_manhattan_distance_between_scanners(scanners)}"
    )


if __name__ == "__main__":
    main()
