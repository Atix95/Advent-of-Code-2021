import os


def load_cave_system(file_name):
    # Load the cave connections line by line and put each pair in a list

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_cave:
        cave_system = [line.split("-") for line in file_cave.read().split("\n")]

    return cave_system


def find_all_paths(cave_system):
    # List of all allowed paths
    paths = []

    # List of all possible path combinations that are stored in lists. The last cave that
    # has been visited in a possible path is checked for neighbours and then if its allowed
    # to add the neighbour/next_cave to the current path, the path is then appended to
    # possible_paths including the neighbour. After that the possible path that has been
    # checked for all neighbours and allowed path continuations is cut from the list of
    # possible paths.
    possible_paths = []

    # Tracking the current path that is taken from possible_paths
    path = []

    # Number of all all paths
    num_of_paths = 0

    for cave_connections in cave_system:
        # Find all caves that leave "start" and add them to the list of possible paths

        if "start" in cave_connections:
            possible_paths.append(
                ["start", (set(cave_connections).difference({"start"}).pop())]
            )

    while len(possible_paths) > 0:
        for cave_connections in cave_system:
            path = [cave for cave in possible_paths[0]]

            if possible_paths[0][-1] in cave_connections:
                # Find all caves that are connected to the last cave of the current
                # possible path. Then, determine the next cave and check if the path
                # is allowed. If the cave is large add it to possible paths. If the
                # path ends with "end" add the path to paths. If the cave is small
                # check, if this cave has already been visited twice. If not create
                # a list of all small caves in path and check whether a small cave has
                # been visited twice. If so and the next cave is not already in the
                # path add it to possible paths.

                next_cave = (
                    set(cave_connections).difference({possible_paths[0][-1]})
                ).pop()

                if next_cave.isupper():
                    possible_paths.append(path + [next_cave])

                elif next_cave == "end" and path + [next_cave] not in paths:
                    paths.append(path + [next_cave])

                elif (
                    next_cave.islower()
                    and path.count(next_cave) < 2
                    and next_cave != "start"
                ):
                    small_caves_in_path = [cave for cave in path[1:] if cave.islower()]

                    if (
                        len(small_caves_in_path) <= len(set(small_caves_in_path))
                        or next_cave not in path
                    ):
                        possible_paths.append(path + [next_cave])

        # Cut the first possible path that has now been
        # checked for all possible path continuations.
        possible_paths = possible_paths[1:]

    num_of_paths = len(paths)

    return num_of_paths


if __name__ == "__main__":
    num_of_paths = find_all_paths(load_cave_system("day_12_input.txt"))

    print(f"The number of all possible paths is: {num_of_paths}")
