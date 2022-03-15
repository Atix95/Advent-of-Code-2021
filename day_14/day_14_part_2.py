import os
import itertools as it


STEPS = 40


def load_manual(file_name):
    # Load the manual and create a dict with the pair insertion rules as well as
    # a string containing the polymer template, on which the rules are applied.
    template = ""
    pair_insertion_rules = {}

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_manual:
        template = file_manual.readline().split()[0]
        pair_insertion_rules = {
            line.split(" -> ")[0]: line.split(" -> ")[1]
            for line in file_manual.read().split("\n")
            if len(line) == 7
        }

    return template, pair_insertion_rules


def pairwise(iterable):
    # pairwise() function which is part of the itertools module since version 3.10.
    # Since I'm on 3.9.7 I'm using the function from the itertools documentation.
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = it.tee(iterable)
    next(b, None)

    return zip(a, b)


def polymer_growth(template, pair_insertion_rules):
    # Function to track the pairs in a dictionary that are created each step.
    # First, the pairs in the template are added to the dict of how frequent the
    # pairs occur to get the starting point. Then the value of each pair is added to
    # the value of the two new pairs in growing_frequency_of_pairs. In addition the
    # value of the newly inserted character is increased by the same amount and is
    # stored in frequency_of_characters. Finally, the increased number of pairs
    # (growing_frequency_of_pairs) is transferred to current_frequency_of_pairs and
    # the running variable growing_frequency_of_pairs is reset.

    growing_frequency_of_pairs = {key: 0 for key in pair_insertion_rules.keys()}
    current_frequency_of_pairs = {key: 0 for key in pair_insertion_rules.keys()}
    frequency_of_characters = {
        character: 0
        for character in set([letter for letter in pair_insertion_rules.values()])
    }

    # Starting point
    for pair_tuple in pairwise(template):
        pair = pair_tuple[0] + pair_tuple[1]
        if pair in current_frequency_of_pairs.keys():
            current_frequency_of_pairs[pair] += 1

    for character in template:
        frequency_of_characters[character] += 1

    for step in range(STEPS):

        for key in current_frequency_of_pairs.keys():

            growing_frequency_of_pairs[
                key[0] + pair_insertion_rules[key]
            ] += current_frequency_of_pairs[key]
            growing_frequency_of_pairs[
                pair_insertion_rules[key] + key[1]
            ] += current_frequency_of_pairs[key]
            frequency_of_characters[
                pair_insertion_rules[key]
            ] += current_frequency_of_pairs[key]

        current_frequency_of_pairs = growing_frequency_of_pairs
        growing_frequency_of_pairs = {key: 0 for key in pair_insertion_rules.keys()}

    return current_frequency_of_pairs, frequency_of_characters


if __name__ == "__main__":
    template, pair_insertion_rules = load_manual("day_14_input.txt")
    frequency_of_pairs, frequency_of_characters = polymer_growth(
        template, pair_insertion_rules
    )

    # Creating the output to check for bugs
    print(
        "Frequency of pairs:\n"
        + "\n".join(
            str(key) + ": " + str(value) for key, value in frequency_of_pairs.items()
        )
        + "\n\nFrequency of characters:\n"
        + "\n".join(
            str(key) + ": " + str(value)
            for key, value in frequency_of_characters.items()
        ),
        "\nThe difference between the most common and the least commong letter is: "
        + f"{max(frequency_of_characters.values()) - min(frequency_of_characters.values())}",
    )
