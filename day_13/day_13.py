import os


def load_manual(file_name):
    # Load the manual which contains the points as well as the fold instructions
    manual = []

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_foil:
        manual = [line.split(",") for line in file_foil.read().split("\n")]

    return manual


def create_points_and_fold_list(manual):
    # Split the manual into lists that contain the
    # points as integers and the fold instructions.
    points = []
    folds = []

    for line in manual:
        try:
            points.append([int(coordinate) for coordinate in line])
        except ValueError:
            if line[0] != "":
                folds.append(line[0])

    return points, folds


def x_height(points):
    # Width of the viewfoil
    return max([x[0] for x in points])


def y_height(points):
    # Length of the viewfoil
    return max([y[1] for y in points])


def create_blank_page(points):
    # Create a blank page in which the points are drawn
    blank_page = []

    for y in range(y_height(points) + 1):
        blank_page.append(["." for x in range(x_height(points) + 1)])

    return blank_page


def create_viewfoil(points):
    # The points are drawn on the blank page to create the viewfoil
    viewfoil = create_blank_page(points)

    for x, y in points:
        viewfoil[y][x] = "#"

    return viewfoil


def first_fold(viewfoil, folds):
    # According to the first fold instruction, fold the paper along the given axis.
    # First, the folding axis has to be determined. After that the paper is folded
    # along this axis by cutting off the half that is folded on the other half. The
    # cut half is then mirrored on the other half (folded_paper) by calculating the
    # distance of each point to the folding axis. Then the point is listed in the
    # first half of the viewfoil (folded_paper) by using the same distance from the
    # mirror axis in the reverse direction.
    folded_paper = []

    if folds[0][11] == "y":
        fold_axis = ("y", int(folds[0][13:]))
    elif folds[0][11]:
        fold_axis = ("x", int(folds[0][13:]))

    if fold_axis[0] == "y":
        for y in range(fold_axis[1]):
            folded_paper.append(viewfoil[y])

        for y, line in enumerate(viewfoil[fold_axis[1] + 1 :], start=fold_axis[1] + 1):
            distance_to_mirror_axis = y - fold_axis[1]

            for x, dot in enumerate(line):
                if dot == "#":
                    folded_paper[fold_axis[1] - distance_to_mirror_axis][x] = "#"

    elif fold_axis[0] == "x":
        for y in range(y_height(points) + 1):
            folded_paper.append([viewfoil[y][x] for x in range(fold_axis[1])])

        for y, line in enumerate(viewfoil):

            for x, dot in enumerate(line[fold_axis[1] + 1 :], start=fold_axis[1] + 1):
                distance_to_mirror_axis = x - fold_axis[1]
                if dot == "#":
                    folded_paper[y][fold_axis[1] - distance_to_mirror_axis] = "#"

    return folded_paper


def count_visible_dots(folded_paper):
    # Count the visible dots (#) in the folded paper
    num_visible_dots = 0

    for line in folded_paper:
        for dot in line:
            if dot == "#":
                num_visible_dots += 1

    return num_visible_dots


if __name__ == "__main__":
    manual = load_manual("day_13_input.txt")
    points, folds = create_points_and_fold_list(manual)
    viewfoil = create_viewfoil(points)
    folded_paper = first_fold(viewfoil, folds)
    num_visible_dots = count_visible_dots(folded_paper)

    print(f"The number of visible points is: {num_visible_dots}")
