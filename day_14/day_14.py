import os
import itertools as it


STEPS = 10


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
    # Create the polymer starting with the template using the pair insertion rules.
    # For this the current template is searched for pairs from the pair insertion
    # rules for each step. If one is found and no pair has been found yet, both
    # characters of the pair with the newly inserted character are added to 
    # growing_polymer. If growing_polymer is not empty, only the last character of
    # the pair will be added to growing_polymer together with the new character.
    # Then the growing_polymer is added to current_template and growing_polymer
    # is reset.
    growing_polymer = ""
    current_template = ""

    current_template = template

    for step in range(STEPS):

        for pair_tuple in pairwise(current_template):
            pair = pair_tuple[0] + pair_tuple[1]

            # Even though each pair tuple taken from the current template is 
            # part of the pair_insertion_rules.keys(), the if query for this
            # matter is obsolete, but is retained for completeness.
            if pair in pair_insertion_rules.keys() and growing_polymer == "":
                growing_polymer += pair[0] + pair_insertion_rules[pair] + pair[1]
            elif pair in pair_insertion_rules.keys():
                growing_polymer += pair_insertion_rules[pair] + pair[1]

        current_template = growing_polymer
        growing_polymer = ""

    return current_template


def count_character_in_polymer(growing_polymer):
    # Count, how often each character occurs in the created polymer
    frequency_of_characters = {}
    counter = 0

    for letter in set(growing_polymer):
        counter = 0

        for character in growing_polymer:
            if letter == character:
                counter += 1

        frequency_of_characters[letter] = counter

    return frequency_of_characters


if __name__ == "__main__":
    template, pair_insertion_rules = load_manual("day_14_input.txt")
    growing_polymer = polymer_growth(template, pair_insertion_rules)
    frequency_of_characters = count_character_in_polymer(growing_polymer)
    print(
        frequency_of_characters,
        "\nThe difference between the most common and the least commong letter is: "
        + f"{max(frequency_of_characters.values()) - min(frequency_of_characters.values())}",
    )
