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


class BinaryNode:
    # Solve the homework assignment using the structure of a binary tree

    def __init__(self, value) -> None:
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def __str__(self) -> str:
        # Visualize the binary tree as snailfish numbers
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
        # Build the binary tree from a snail number
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

    def add_tree(self, tree_to_be_added):
        # Create a new tree to which the two trees that are to
        # be added are added as the left and right BinaryNode.
        left_tree = self
        right_tree = tree_to_be_added

        root = BinaryNode(None)
        root.add_left_node(left_tree)
        root.add_right_node(right_tree)

        return root

    def depth(self) -> int:
        # Return the depth of the entire tree
        if self.is_leaf():
            return 0
        return max(self.left.depth() + 1, self.right.depth() + 1)

    def depth_of_branch(self) -> int:
        # Return the depth of the current branch/leaf
        if self.parent == None:
            return 0
        return self.parent.depth_of_branch() + 1

    def get_all_leafs(self):
        # Get all leafs and return them in a list
        list_of_leafs = []

        if self.is_leaf():
            return [self]

        if self.left != None:
            list_of_leafs.extend(self.left.get_all_leafs())
        if self.right != None:
            list_of_leafs.extend(self.right.get_all_leafs())

        return list_of_leafs

    def get_two_leftmost_exploading_leafs_incl_idx(self) -> List[Tuple]:
        # Return the two leftmost exploading leafs as pairs
        # with the respective position in list_of_leafs.
        exploading_leafs = []

        for leaf_idx, exploading_leaf in enumerate(self.get_all_leafs()):
            if exploading_leaf.depth_of_branch() > 4 and len(exploading_leafs) < 4:
                exploading_leafs.extend([leaf_idx, exploading_leaf])

        return exploading_leafs

    def reset_parent_after_explosion(self):
        # Set the left and right BinaryNodes of the parent BinaryNode
        # to None as well as its value to 0 after an explosion occured.
        self.parent.left = None
        self.parent.right = None
        self.parent.value = 0

    def explosion(self):
        # Explode the leftmost pair. First, get the leafs of the exploding pair with
        # the respective position in the list_of_leafs. Then add the values to the value
        # to the left or right of it, if they exit. The value of the parent BinaryNode is
        # then set to 0 and its left and right BinaryNode are set to None.
        (
            left_idx,
            left_leaf,
            right_idx,
            right_leaf,
        ) = self.get_two_leftmost_exploading_leafs_incl_idx()

        list_of_leafs = self.get_all_leafs()

        if left_idx - 1 >= 0:
            list_of_leafs[left_idx - 1].value += left_leaf.value
        if right_idx <= len(list_of_leafs) - 2:
            list_of_leafs[right_idx + 1].value += right_leaf.value

        left_leaf.reset_parent_after_explosion()

    def get_splitting_leaf(self):
        # Get the leftmost value in the list_of_leafs that is to be splitted
        splitting_leaf = None

        for leaf in self.get_all_leafs():
            if leaf.value >= 10:
                splitting_leaf = leaf
                break

        return splitting_leaf

    def split(self):
        # Split the leftmost value in the list_of_leafs. A new BinaryNode is created
        # for the left and right BinaryNode of the BinaryNode that is to be splitted
        # (splitting_leaf). The value of the left BinaryNode is rounded down and the
        # value of the right BinaryNode is rounded up. Lastly, the value of the
        # BinaryNode that was splitted is set to None.
        splitting_leaf = self.get_splitting_leaf()

        splitting_leaf.add_left_node(BinaryNode(splitting_leaf.value // 2))
        splitting_leaf.add_right_node(BinaryNode((splitting_leaf.value + 1) // 2))
        splitting_leaf.value = None

    def reduce(self):
        # Reduce the snailfish number. An explosion is performed until all of them
        # are resolved. Then the splitting of the snailfish numbers is performed.
        # If an exploding pair is produced as a result of a split, the pair will
        # be exploded before further splits are executed. The approach with a while
        # loop is chosen, as a recursive call of reduce() leads to exceeding the
        # maximum recursive calls.
        while True:

            if self.depth() > 4:
                self.explosion()
                continue

            if self.get_splitting_leaf() != None:
                self.split()
                continue

            break

        return self

    def magnitude(self) -> int:
        # Calculate the magnitude of a snailnumber. The magnitude of a pair is the
        # 3 times the magnitude of the elemnt plus 2 times the magnitude of the right
        # element. If the element is a leaf the magnitude is just its value.
        if self.is_leaf():
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


def main():
    # Call all the necessary functions to do the homework assignment
    snail_numbers = load_snail_numbers("day_18_input.txt")

    sum = BinaryNode.build_binary_tree(snail_numbers.pop(0))

    for snail_number in snail_numbers:
        sum = sum.add_tree(BinaryNode.build_binary_tree(snail_number))
        sum.reduce()

    print(f"The final sum is: {sum}")
    print(f"The magnitude of the final sum is: {sum.magnitude()}")


if __name__ == "__main__":
    main()
