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


def folding(viewfoil, folds):
    # According to the fold instructions, fold the paper along the desired axis. First,
    # the folding axis has to be determined. After that the paper is folded along this
    # axis by cutting off the half that is folded on the other half. The cut half is then
    # mirrored on the other half (folded_paper) by calculating the distance of each point
    # to the folding axis. Then the point is listed in the first half of the viewfoil
    # (folded_paper) by using the same distance from the mirror axis in reverse direction.
    # For the next fold the recently folded paper is stored in viewfoil_to_fold and the
    # list folded_paper is reset, where the next fold will be performed.
    folded_paper = []
    viewfoil_to_fold = [line for line in viewfoil]

    for fold in folds:
        fold_axis = int(fold[13:])

        if fold[11] == "y":
            for y in range(fold_axis):
                folded_paper.append(viewfoil_to_fold[y])

            for y, line in enumerate(
                viewfoil_to_fold[fold_axis + 1 :], start=fold_axis + 1
            ):
                distance_to_mirror_axis = y - fold_axis

                for x, dot in enumerate(line):
                    if dot == "#":
                        folded_paper[fold_axis - distance_to_mirror_axis][x] = "#"

        elif fold[11] == "x":
            for y in range(len(viewfoil_to_fold)):
                folded_paper.append([viewfoil_to_fold[y][x] for x in range(fold_axis)])

            for y, line in enumerate(viewfoil_to_fold):

                for x, dot in enumerate(line[fold_axis + 1 :], start=fold_axis + 1):
                    distance_to_mirror_axis = x - fold_axis
                    if dot == "#":
                        folded_paper[y][fold_axis - distance_to_mirror_axis] = "#"

        viewfoil_to_fold = [line for line in folded_paper]
        folded_paper = []

    return viewfoil_to_fold


if __name__ == "__main__":
    manual = load_manual("day_13_input.txt")
    points, folds = create_points_and_fold_list(manual)
    viewfoil = create_viewfoil(points)
    viewfoil_to_fold = folding(viewfoil, folds)

    print(
        f"The code to activate the infrared thermal imaging camera system is:\n"
        + "\n".join(str(line) for line in viewfoil_to_fold),
    )
