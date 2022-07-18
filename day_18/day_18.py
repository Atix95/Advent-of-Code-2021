import json
import os
from typing import List, Tuple


def load_snail_numbers(file_name):
    # Load the snail numbers to add up as lists
    snail_numbers = []

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    with open(file_path, "r", encoding="utf-8") as file_snail:
        snail_numbers = [json.loads(numbers) for numbers in file_snail.readlines()]

    return snail_numbers


def pairwise(iterable):
    x = iter(iterable)
    return zip(x, x)


class BinaryNode:
    def __init__(self, value) -> None:
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def __str__(self) -> str:
        if self.is_leaf():
            return str(self.value)
        return f"[{str(self.left)}, {str(self.right)}]"

    def is_leaf(self) -> bool:
        return isinstance(self.value, int)

    def is_branch(self) -> bool:
        return isinstance(self, BinaryNode)

    def add_left_branch(self, left_branch: List) -> None:
        self.left = self.build_binary_tree(left_branch)
        self.left.parent = self

    def add_right_branch(self, right_branch: List) -> None:
        self.right = self.build_binary_tree(right_branch)
        self.right.parent = self

    @classmethod
    def build_binary_tree(cls, snail_number):
        root = cls(None)

        if isinstance(snail_number, int):
            root.value = snail_number
            return root

        left_branch, right_branch = snail_number
        root.add_left_branch(left_branch)
        root.add_right_branch(right_branch)

        return root

    def flatten(self) -> List[int]:
        # This is just to test and learn about classes in Python
        values = []

        if self.is_leaf():
            return [self.value]

        values.extend(self.left.flatten())
        values.extend(self.right.flatten())

        return values

    def add_left_node(self, left_tree):
        self.left = left_tree
        self.left.parent = self

    def add_right_node(self, right_tree):
        self.right = right_tree
        self.right.parent = self

    def add_trees(self, tree_to_be_added):
        left_tree = self
        right_tree = tree_to_be_added

        root = BinaryNode(None)
        root.add_left_node(left_tree)
        root.add_right_node(right_tree)

        return root

    def depth(self) -> int:
        if self.is_leaf():
            return 0
        return max(self.left.depth() + 1, self.right.depth() + 1)

    def depth_of_branch(self) -> int:
        if self.parent == None:
            return 0
        return self.parent.depth_of_branch() + 1

    def get_all_leafs(self):
        list_of_leafs = []

        if self.is_leaf():
            return [self]

        if self.left != None:
            list_of_leafs.extend(self.left.get_all_leafs())
        if self.right != None:
            list_of_leafs.extend(self.right.get_all_leafs())

        return list_of_leafs

    def get_all_exploading_leafs(self) -> List[Tuple]:
        exploading_leafs = []

        for leaf_idx, exploading_leaf in enumerate(self.get_all_leafs()):
            if exploading_leaf.depth_of_branch() > 4:
                exploading_leafs.append((leaf_idx, exploading_leaf))

        return exploading_leafs

    def explosion(self):
        exploading_leafs = self.get_all_exploading_leafs()
        list_of_leafs = self.get_all_leafs()

        for left_leaf_pair, right_leaf_pair in pairwise(exploading_leafs):
            left_idx, left_leaf = left_leaf_pair
            right_idx, right_leaf = right_leaf_pair

            if left_idx - 1 >= 0:
                list_of_leafs[left_idx - 1].value += left_leaf.value
            if right_idx <= len(list_of_leafs) - 2:
                list_of_leafs[right_idx + 1].value += right_leaf.value

            left_leaf.parent.left = None
            left_leaf.parent.right = None
            left_leaf.parent.value = 0

    def reduce(self):
        # Check for explosions
        if self.depth() > 4:
            self.explosion()

        return self

    def magnitude(self) -> int:
        if self.is_leaf():
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


if __name__ == "__main__":
    snail_numbers = load_snail_numbers("day_18_example_input.txt")
    # print("\n".join(str(line) for line in snail_numbers))
    # print("Snail numbers added:")
    # print(add_snail_numbers([7, [6, [5, [4, [3, 2]]]]]))
    # print(Node.build_binary_tree(snail_numbers[0]))

    # [[[[[9, 8], 1], 2], 3], 4]
    # [7, [6, [5, [4, [3, 2]]]]]
    x = BinaryNode.build_binary_tree([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
    print(x)

