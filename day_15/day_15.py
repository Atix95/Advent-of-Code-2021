import os


def load_risk_levels(file_name):
    # Create a list of each digit in the risk levels
    split_num_into_digits = lambda num: [int(digit) for digit in str(num)]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_risk:
        risk_levels = [
            split_num_into_digits(line)
            for line in file_risk.read().split("\n")
        ]

    return risk_levels


if __name__ == "__main__":
    print(load_risk_levels("day_15_example_input.txt"))