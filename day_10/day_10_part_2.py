import os


BRACKET_PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}


def load_navigation(file_name):
    # Load the navigation subsystem line by line
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_navigation:
        navigation_subsystem = [line for line in file_navigation.read().split("\n")]

    return navigation_subsystem


def delete_corrupted_lines(navigation_subsystem):
    # Track found characters and indices of corrupted lines
    found_characters = []
    corrupted_lines = []

    # List of all lines from which the corrupted lines are
    # deleted so that only the incomplete lines remain.
    incomplete_lines = navigation_subsystem

    for index, line in enumerate(navigation_subsystem):
        found_characters = []

        for character in line:

            if character in BRACKET_PAIRS.keys():
                found_characters.append(character)
            elif (
                character in BRACKET_PAIRS.values()
                and character == BRACKET_PAIRS[found_characters[-1]]
            ):
                found_characters = found_characters[:-1]
            else:
                corrupted_lines.append(index)
                break

    for corrupted_index in reversed(corrupted_lines):
        incomplete_lines.pop(corrupted_index)

    return incomplete_lines


def repair_incomplete_lines(incomplete_lines):
    # Score table to determine the autocomplete error score
    score_table = {")": 1, "]": 2, "}": 3, ">": 4}
    autocomplete_score = 0
    autocomplete_score_table = []

    # Track found characters
    found_characters = []

    for line in incomplete_lines:
        # Reset the list of found characters and autocomplete score
        found_characters = []
        autocomplete_score = 0

        for character in line:
            if character in BRACKET_PAIRS.keys():
                found_characters.append(character)
            elif (
                character in BRACKET_PAIRS.values()
                and character == BRACKET_PAIRS[found_characters[-1]]
            ):
                found_characters = found_characters[:-1]

        for character in reversed(found_characters):
            autocomplete_score = (
                autocomplete_score * 5 + score_table[BRACKET_PAIRS[character]]
            )

        autocomplete_score_table.append(autocomplete_score)

    autocomplete_score_table.sort()

    return autocomplete_score_table[len(incomplete_lines) // 2]


if __name__ == "__main__":
    incomplete_lines = delete_corrupted_lines(load_navigation("day_10_input.txt"))
    autocomplete_middle_score = repair_incomplete_lines(incomplete_lines)

    print(f"The middle autocomplete score is: {autocomplete_middle_score}")
