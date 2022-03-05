import os


def load_heightmap(file_name):
    # Create a list of each digit in the heightmap with a
    # counter that records which digit belongs to which basin.
    split_num_into_digits = lambda num: [[int(digit), -1] for digit in str(num)]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_height:
        heightmap = [
            split_num_into_digits(line) for line in file_height.read().split("\n")
        ]

    return heightmap


def find_basin(heightmap):
    multiple_of_three_largest_basins = 0
    basin_size = 0
    basin_sizes = []

    # Collecting nearest neighbours of a digit that are not 9
    # as well as the first digit found of a new basin
    list_of_neighbours = []

    # Counter to track which digit belongs to which basin
    basin_counter = 0

    for v_index, line in enumerate(heightmap):
        for h_index, digit in enumerate(line):
            # Check from left to right and then from top to bottom.
            # If a digit is found that does not yet belong to a basin
            # it is added to list_of_neighbours and is checked in all
            # directions for nearest neighbours that are not 9. If such
            # a neighbour is found it is added to list_of_neighbours.
            # The element will then be removed from the list and the
            # remaining contents of list_of_neighbours are then checked
            # again for nearest neighbours that are not 9.

            # Reset the basin size counter
            basin_size = 0

            if digit[1] < 0 and digit[0] != 9:
                list_of_neighbours.append((digit, v_index, h_index))

                while len(list_of_neighbours) > 0:
                    v_run_variable = list_of_neighbours[0][1]
                    h_run_variable = list_of_neighbours[0][2]

                    if (
                        h_run_variable + 2 <= len(line)
                        and heightmap[v_run_variable][h_run_variable + 1][1] < 0
                        and heightmap[v_run_variable][h_run_variable + 1][0] != 9
                        and (
                            heightmap[v_run_variable][h_run_variable + 1],
                            v_run_variable,
                            h_run_variable + 1,
                        )
                        not in list_of_neighbours
                    ):
                        # Check if a neighbour to the right exists and if
                        # its not already in a basin and not 9. If it has
                        # not yet been added to the list, it will be added.
                        list_of_neighbours.append(
                            (
                                heightmap[v_run_variable][h_run_variable + 1],
                                v_run_variable,
                                h_run_variable + 1,
                            )
                        )

                    if (
                        h_run_variable - 1 >= 0
                        and heightmap[v_run_variable][h_run_variable - 1][1] < 0
                        and heightmap[v_run_variable][h_run_variable - 1][0] != 9
                        and (
                            heightmap[v_run_variable][h_run_variable - 1],
                            v_run_variable,
                            h_run_variable - 1,
                        )
                        not in list_of_neighbours
                    ):
                        # Check if a neighbour to the left exists and if
                        # its not already in a basin and not 9. If it has
                        # not yet been added to the list, it will be added.
                        list_of_neighbours.append(
                            (
                                heightmap[v_run_variable][h_run_variable - 1],
                                v_run_variable,
                                h_run_variable - 1,
                            )
                        )

                    if (
                        v_run_variable + 2 <= len(heightmap)
                        and heightmap[v_run_variable + 1][h_run_variable][1] < 0
                        and heightmap[v_run_variable + 1][h_run_variable][0] != 9
                        and (
                            heightmap[v_run_variable + 1][h_run_variable],
                            v_run_variable + 1,
                            h_run_variable,
                        )
                        not in list_of_neighbours
                    ):
                        # Check if a neighbour to the bottom exists and if
                        # its not already in a basin and not 9. If it has
                        # not yet been added to the list, it will be added.
                        list_of_neighbours.append(
                            (
                                heightmap[v_run_variable + 1][h_run_variable],
                                v_run_variable + 1,
                                h_run_variable,
                            )
                        )

                    if (
                        v_run_variable - 1 >= 0
                        and heightmap[v_run_variable - 1][h_run_variable][1] < 0
                        and heightmap[v_run_variable - 1][h_run_variable][0] != 9
                        and (
                            heightmap[v_run_variable - 1][h_run_variable],
                            v_run_variable - 1,
                            h_run_variable,
                        )
                        not in list_of_neighbours
                    ):
                        # Check if a neighbour to the top exists and if
                        # its not already in a basin and not 9. If it has
                        # not yet been added to the list, it will be added.
                        list_of_neighbours.append(
                            (
                                heightmap[v_run_variable - 1][h_run_variable],
                                v_run_variable - 1,
                                h_run_variable,
                            )
                        )

                    heightmap[v_run_variable][h_run_variable][1] = basin_counter
                    list_of_neighbours = list_of_neighbours[1:]
                    basin_size += 1

                # Basin has been found. Raise basin counter and add
                # the size of the basin to the list of basin sizes.
                basin_sizes.append(basin_size)
                basin_counter += 1

    # Sort the list of basin sizes and multiply the last
    # three elements together which are the largest values
    basin_sizes.sort()
    multiple_of_three_largest_basins = (
        basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]
    )

    return multiple_of_three_largest_basins


if __name__ == "__main__":
    multiple_of_three_largest_basins = find_basin(load_heightmap("day_9_input.txt"))

    print(
        f"The product of the three largest basins is: {multiple_of_three_largest_basins}"
    )
