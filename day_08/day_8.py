import os


def load_display_patterns(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_patterns:
        display_patterns = [
            line.replace("|", "").split()
            for line in file_patterns.read().strip().split("\n")
        ]

    return display_patterns


def find_easy_digits(display_patterns):
    num_of_easy_digits = 0

    for display in range(len(display_patterns)):
        for output in range(10, 14):
            if len(display_patterns[display][output]) == 2:  # number 1
                num_of_easy_digits += 1
            elif len(display_patterns[display][output]) == 3:  # number 7
                num_of_easy_digits += 1
            elif len(display_patterns[display][output]) == 4:  # number 4
                num_of_easy_digits += 1
            elif len(display_patterns[display][output]) == 7:  # number 8
                num_of_easy_digits += 1

    return num_of_easy_digits


if __name__ == "__main__":
    num_of_easy_digits = find_easy_digits(load_display_patterns("day_8_input.txt"))

    print(f"The number of unique instances of digits is: {num_of_easy_digits}")
