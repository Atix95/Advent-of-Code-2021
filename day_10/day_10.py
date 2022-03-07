import os


def load_navigation(file_name):
    # Load the navigation subsystem line by line
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_navigation:
        navigation_subsystem = [line for line in file_navigation.read().split("\n")]

    return navigation_subsystem


def find_corrupted_lines(navigation_subsystem):
    # Dictionary with bracket pairs
    bracket_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}

    # Score table to determine the syntax error score
    score_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
    syntax_error_score = 0

    # Track found characters
    found_characters = []

    for line in navigation_subsystem:
        found_characters = []

        for character in line:

            if character in bracket_pairs.keys():
                found_characters.append(character)
            elif (
                character in bracket_pairs.values()
                and character == bracket_pairs[found_characters[-1]]
            ):
                found_characters = found_characters[:-1]
            else:
                # Print an error message as its shown in the task
                # and add the score of the unmatching bracket
                print(
                    f"Expected {bracket_pairs[found_characters[-1]]}, "
                    + "but found {character} instead."
                )
                syntax_error_score += score_table[character]
                break

    return syntax_error_score


if __name__ == "__main__":
    syntax_error_score = find_corrupted_lines(load_navigation("day_10_input.txt"))

    print(f"The syntax error score is: {syntax_error_score}")
