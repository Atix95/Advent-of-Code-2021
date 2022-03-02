import os


def load_display_patterns(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_patterns:
        display_patterns = [
            line.replace("|", "").split()
            for line in file_patterns.read().strip().split("\n")
        ]

    return display_patterns


def sort_patterns(display_patterns):
    # alphabetical sorting of the patterns

    for display in range(len(display_patterns)):
        for output in range(14):
            sorted_string = ""
            display_patterns[display][output] = sorted_string.join(
                sorted(display_patterns[display][output])
            )

    return display_patterns


def decode_display(display_patterns):
    sum_of_output_entries = 0

    for display in range(len(display_patterns)):
        zero_six_nine_string = []
        two_three_five_string = []
        output_entry = ""

        for pattern in range(0, 10):
            # Find difficult numbers and those for identfying them
            if len(display_patterns[display][pattern]) == 2:
                # Number 1
                one_string = display_patterns[display][pattern]

            elif len(display_patterns[display][pattern]) == 4:
                # Number 4
                four_string = display_patterns[display][pattern]

            elif len(display_patterns[display][pattern]) == 5:
                # Number 2, 3 and 5
                two_three_five_string.append(display_patterns[display][pattern])

            elif len(display_patterns[display][pattern]) == 6:
                # Number 0, 6 and 9
                zero_six_nine_string.append(display_patterns[display][pattern])

        # Identification string used to distinguish difficult numbers, since the
        # two left over segments from number 4, if the segments of number 1 are
        # subtracted, as well as the segments from number 1 can be used to
        # identify the numbers in the triplets
        identification_string = four_string.replace(one_string[0], "").replace(
            one_string[1], ""
        )

        for output in range(10, 14):
            # Decode the output
            if len(display_patterns[display][output]) == 2:
                # Number 1
                output_entry += "1"

            elif len(display_patterns[display][output]) == 3:
                # Number 7
                output_entry += "7"

            elif len(display_patterns[display][output]) == 4:
                # Number 4
                output_entry += "4"

            elif len(display_patterns[display][output]) == 5:
                # Number 2, 3 and 5
                if (
                    len(
                        display_patterns[display][output]
                        .replace(one_string[0], "")
                        .replace(one_string[1], "")
                    )
                    == 3
                ):
                    # Number 3, since the whole sequence for number 1
                    # only appears in number 3 out of 2, 3 and 5
                    output_entry += "3"
                elif (
                    len(
                        display_patterns[display][output]
                        .replace(identification_string[0], "")
                        .replace(identification_string[1], "")
                    )
                    == 3
                ):
                    # Number 5, since the whole Identification string
                    # only appears in number 5 out of 2, 3 and 5
                    output_entry += "5"
                else:
                    # Last possibility from the triplet, number 2
                    output_entry += "2"

            elif len(display_patterns[display][output]) == 6:  # Number 0, 6 and 9
                if (
                    len(
                        display_patterns[display][output]
                        .replace(identification_string[0], "")
                        .replace(identification_string[1], "")
                    )
                    == 5
                ):
                    # Number 0, since the whole Identification string
                    # only appears in number 0 out of 0, 6 and 9
                    output_entry += "0"
                elif (
                    len(
                        display_patterns[display][output]
                        .replace(one_string[0], "")
                        .replace(one_string[1], "")
                    )
                    == 4
                ):
                    # Number 9, since the whole sequence for number 1
                    # only appears in number 9 out of 0, 6 and 9
                    output_entry += "9"
                else:
                    # Last possibility from the triplet, number 6
                    output_entry += "6"

            elif len(display_patterns[display][output]) == 7:
                output_entry += "8"

        sum_of_output_entries += int(output_entry)

    return sum_of_output_entries


if __name__ == "__main__":
    print(
        "The sum of all output entries is: "
        + f"{decode_display(sort_patterns(load_display_patterns('day_8_input.txt')))}"
    )
