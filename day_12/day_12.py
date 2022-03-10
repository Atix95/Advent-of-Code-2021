import os


def load_cave_system(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__, file_name)))
    with open(file_path, "r", encoding="utf-8") as file_cave:
        cave_system = [line for line in file_cave.read()]

    return cave_system
