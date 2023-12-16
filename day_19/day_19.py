import os
import re


def load_input(file_name: str) -> dict:
    scanners = {}

    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))

    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        if line.startswith("--- scanner"):
            scanner_number = int(re.findall(r"\d+", line)[0])
            scanners[scanner_number] = []
        elif line != "":
            scanners[scanner_number].append([int(number) for number in line.split(",")])

    return scanners


class Scanner:
    def __init__(self, scanner_number: int, readings):
        self.scanner_number = scanner_number
        self.readings = readings

    def __repr__(self):
        output = ""
        output += f"Scanner {self.scanner_number}:\n"
        for reading in self.readings:
            output += f"{reading}\n"
        return output


scanners = []
input = load_input("day_19_example_input.txt")

for scanner_number in input.keys():
    scanners.append(Scanner(scanner_number, input[scanner_number]))
