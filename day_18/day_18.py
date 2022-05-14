import json
import os
from typing import List


def load_snail_numbers(file_name):
    # Load the snail numbers to add up as lists
    snail_numbers = []

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    with open(file_path, "r", encoding="utf-8") as file_snail:
        snail_numbers = [json.loads(numbers) for numbers in file_snail.readlines()]

    return snail_numbers


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        return f"[{str(self.left)}, {str(self.right)}]"

    def is_leaf(self) -> bool:
        return isinstance(self.value, int)

    def is_branch(self) -> bool:
        return isinstance(self, Node)

    def flatten(self) -> List[int]:
        values = []

        if self.is_leaf():
            return [self.value]

        values.extend(self.left.flatten())
        values.extend(self.right.flatten())

        return values

    def depth(self) -> int:
        if self.is_leaf():
            return 0
        return max(self.left.depth() + 1, self.right.depth() + 1)

    def depth_branches(self) -> int:
        return

    def add_trees(self, tree_to_be_added):
        original_tree = self

        root = Node(None)
        root.left = original_tree
        root.right = tree_to_be_added

        return root

    def magnitude(self) -> int:
        if self.is_leaf():
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @classmethod
    def build_binary_tree(cls, snail_number):
        root = cls(None)

        if isinstance(snail_number, int):
            root.value = snail_number
            return root

        root.left = cls.build_binary_tree(snail_number[0])
        root.right = cls.build_binary_tree(snail_number[1])

        return root

    def get_all_leafs(self):
        list_of_leafs = []

        if self.is_leaf():
            return [self]

        if self.left != None:
            list_of_leafs.extend(self.left.get_all_leafs())
        if self.right != None:
            list_of_leafs.extend(self.right.get_all_leafs())

        return list_of_leafs

    def reduce(self):
        # Check for explosions
        if self.depth() > 4:
            leafs = self.get_all_leafs()
            return

        return


def check_if_snail_number_is_nested(x, y, x_depth=0, y_depth=0):

    if isinstance(x, list):
        x_depth += 1
        print("right", x, x_depth)
        if x_depth < 4:
            check_if_snail_number_is_nested(x[0], x[1], x_depth, y_depth)
        elif x_depth == 4:
            # explosion!
            add_left, add_right = x
            print(add_left, add_right, x_depth, y_depth)

    if isinstance(y, list):
        y_depth += 1
        print("left", y, y_depth)
        if y_depth < 4:
            check_if_snail_number_is_nested(y[0], y[1], x_depth, y_depth)
        elif y_depth == 4:
            # explosion!
            add_left, add_right = y
            print(add_left, add_right, x_depth, y_depth)

    return


def add_snail_numbers(snail_numbers):

    snail_number_add = snail_numbers[0]
    print(snail_number_add)
    for snail_number in snail_numbers[1:]:
        snail_number_add = [snail_number_add, snail_number]
        # Check for explosions and splits. Since splits should be simpler, start with them!
        x, y = snail_number_add
        print(snail_number_add)
        check_if_snail_number_is_nested(x, y)

    return snail_number_add


if __name__ == "__main__":
    snail_numbers = load_snail_numbers("day_18_example_input.txt")
    # print("\n".join(str(line) for line in snail_numbers))
    # print("Snail numbers added:")
    # print(add_snail_numbers([7, [6, [5, [4, [3, 2]]]]]))
    # print(Node.build_binary_tree(snail_numbers[0]))

    # [[[[[9, 8], 1], 2], 3], 4]
    # [7, [6, [5, [4, [3, 2]]]]]
    # x = Node.build_binary_tree([7, [6, [5, [4, [3, 2]]]]])
    x = Node.build_binary_tree(9)
    print(x)
    print(x.depth())
    print(x.get_all_leafs())

    """
        1. input: Knoten mit einer Zahl
        2. input: Knoten mit zwei Kindern (Zahlen)
        3. input: Knoten mit zwei Kindern, die jeweils zwei Kinder haben
        weitere Ebenen
    """
