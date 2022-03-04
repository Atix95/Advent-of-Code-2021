import os


def load_heightmap(file_name):
    # Create a tuple of each digit in the heightmap with a boolean, that
    # is False, if the digit has not yet been checked to be a lowpoint.
    # This is done to prevent a lowpoint to be counted multiple times.
    split_num_into_digits = lambda num: [[int(digit), False] for digit in str(num)]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_height:
        heightmap = [
            split_num_into_digits(line) for line in file_height.read().split("\n")
        ]

    return heightmap


def find_lowpoint(heightmap):
    sum_of_lowpoints = 0
    debug = []

    for v_index, line in enumerate(heightmap):
        for h_index, digit in enumerate(line):
            path = []
            if (
                digit[1] == False
                and h_index < len(line) - 1
                and v_index < len(heightmap) - 1
            ):
                while digit[0] > line[h_index + 1][0]:
                    if line[h_index + 1][1] == False:
                        digit[1] = True
                        h_index += 1
                        digit = line[h_index]
                        path.append(digit[0])
                        if h_index + 2 >= len(line):
                            break
                    else:
                        break

                v_run_variable = v_index
                if v_run_variable < len(heightmap):
                    while digit[0] > heightmap[v_run_variable + 1][h_index][0]:
                        if heightmap[v_run_variable + 1][h_index][1] == False:
                            digit[1] = True
                            v_run_variable += 1
                            digit = heightmap[v_run_variable][h_index]
                            path.append(digit[0])
                            if v_run_variable + 2 >= len(heightmap):
                                break
                        else:
                            break
            elif (
                digit[1] == False
                and h_index < len(line) - 1
                and v_index >= len(heightmap) - 1
            ):
                while digit[0] > line[h_index + 1][0]:
                    if line[h_index + 1][1] == False:
                        digit[1] = True
                        h_index += 1
                        digit = line[h_index]
                        path.append(digit[0])
                        if h_index + 2 >= len(line):
                            break
                    else:
                        break
                v_run_variable = v_index
            elif (
                digit[1] == False
                and h_index >= len(line) - 1
                and v_index < len(heightmap) - 1
            ):
                v_run_variable = v_index
                if v_run_variable < len(heightmap):
                    while digit[0] > heightmap[v_run_variable + 1][h_index][0]:
                        if heightmap[v_run_variable + 1][h_index][1] == False:
                            digit[1] = True
                            v_run_variable += 1
                            digit = heightmap[v_run_variable][h_index]
                            path.append(digit[0])
                            if v_run_variable + 2 >= len(heightmap):
                                break
                        else:
                            break
            # Cases to check for possible lowpoint depending on location in heightmap:
            # Middle
            # Top line
            # Bottom line
            # Left line
            # Right line
            # Top left corner
            # Top right corner
            # Bottom left corner
            # Bottom right corner

            # print(h_index, v_run_variable)
            if 0 < h_index < len(line) - 1 and 0 < v_run_variable < len(heightmap) - 1:
                # Middle of the heightmap -> check in all directions
                if (
                    digit[0] < heightmap[v_run_variable][h_index + 1][0]
                    and digit[0] < heightmap[v_run_variable][h_index - 1][0]
                    and digit[0] < heightmap[v_run_variable + 1][h_index][0]
                    and digit[0] < heightmap[v_run_variable - 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif 0 < h_index < len(line) - 1 and v_run_variable <= 0:
                # Top line of the heightmap -> check to the left, right and bottom
                if (
                    digit[0] < heightmap[v_run_variable][h_index - 1][0]
                    and digit[0] < heightmap[v_run_variable][h_index + 1][0]
                    and digit[0] < heightmap[v_run_variable + 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif 0 < h_index < len(line) - 1 and v_run_variable >= len(heightmap) - 1:
                # Bottom line of the heightmap -> check to the left, right and top
                if (
                    digit[0] < heightmap[v_run_variable][h_index - 1][0]
                    and digit[0] < heightmap[v_run_variable][h_index + 1][0]
                    and digit[0] < heightmap[v_run_variable - 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif h_index <= 0 and 0 < v_run_variable < len(heightmap) - 1:
                # Left line of the heightmap -> check to the right, top and bottom
                if (
                    digit[0] < heightmap[v_run_variable][h_index + 1][0]
                    and digit[0] < heightmap[v_run_variable - 1][h_index][0]
                    and digit[0] < heightmap[v_run_variable + 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif h_index >= len(line) - 1 and 0 < v_run_variable < len(heightmap) - 1:
                # Right line of the heightmap -> check to the left, top and bottom
                if (
                    digit[0] < heightmap[v_run_variable][h_index - 1][0]
                    and digit[0] < heightmap[v_run_variable - 1][h_index][0]
                    and digit[0] < heightmap[v_run_variable + 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif h_index <= 0 and v_run_variable <= 0:
                # Top left corner of the heightmap -> check to right and bottom
                if (
                    digit[0] < heightmap[v_run_variable][h_index + 1][0]
                    and digit[0] < heightmap[v_run_variable + 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif h_index >= len(line) - 1 and v_run_variable <= 0:
                # Top right corner of the heightmap -> check to left and bottom
                if (
                    digit[0] < heightmap[v_run_variable][h_index - 1][0]
                    and digit[0] < heightmap[v_run_variable + 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif h_index <= 0 and v_run_variable >= len(heightmap) - 1:
                # Bottom left corner of the heighmap -> check to right and top
                if (
                    digit[0] < heightmap[v_run_variable][h_index + 1][0]
                    and digit[0] < heightmap[v_run_variable - 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)
            elif h_index >= len(line) - 1 and v_run_variable >= len(heightmap) - 1:
                # Bottom right corner of the heighmap -> check to left and top
                if (
                    digit[0] < heightmap[v_run_variable][h_index - 1][0]
                    and digit[0] < heightmap[v_run_variable - 1][h_index][0]
                    and digit[1] == False
                ):
                    sum_of_lowpoints += digit[0] + 1
                    digit[1] = True
                    debug.append((digit[0], h_index, v_run_variable))
                    print(path)

    print(debug)
    for line in heightmap:
        print(line)
    return sum_of_lowpoints


if __name__ == "__main__":
    sum_of_lowpoints = find_lowpoint(load_heightmap("day_9_input.txt"))

    print(f"The sum of all lowpoints is: {sum_of_lowpoints}")
