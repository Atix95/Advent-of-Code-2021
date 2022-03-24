import os


def load_target_area(file_name):
    # Load the target area and return a list of the intervals in x- and y-direction
    target_area = []

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    with open(file_path, "r", encoding="utf-8") as file_target:
        target_string = file_target.readline().strip("target area: x=")

    for coordinate_string in target_string.split(", y="):
        coordinate = [int(value) for value in coordinate_string.split("..")]
        target_area.append(coordinate)

    return target_area


def find_highest_point(target_area):
    # Calculate all possible velocities and determine the heighest point reached among
    # them. First the target area as well as the drag in both directions and the start
    # position are defined. A velocity that reaches the target are is stored in velocities.
    # The heights reached during a trajectory are stored in the set heights and the highest
    # value among them is stored in max_heights, if the probe hits the target area. The step
    # variable is the step size between each calculation step. Then all possible permutations
    # of (v_x, v_y) are tried for the probe hitting the target for a selected range of values.
    # If v_x is greater than the maximum of the target area in x direction, v_x has to be
    # between them (0, max(target_area_x)), because otherwise it will overshoot the target area
    # in one step. The same goes for the lower limit of v_y -> min(target_area_y). The upper
    # limit must be guessed and was chosen to be the negative of min(target_area_y). The reason
    # being, that if the probe is shot under a high angle, v_x has to be small in order for the
    # probe to hit the target area, because a lot of steps are involved for the probe to get back
    # down, which means v_x has to be 0 after only a couple of steps. Since a lot of steps are
    # involved, v_y will high negative values due to gravity, which makes it very likely for
    # the probe to overshoot the target area in y direction.
    target_area_x, target_area_y = target_area
    drag_x, drag_y = (-1, -1)
    s_x, s_y = (0, 0)

    velocities = []
    heights = set()
    max_heights = []
    step = 1

    for v_x in range(max(target_area_x) + 1):

        for v_y in range(min(target_area_y), -min(target_area_y) + 1):
            s_x, s_y = (0, 0)
            heights = set()
            v_x_drag, v_y_drag = (v_x, v_y)

            while True:
                # Calculate (s_x, s_y) after one step. The height s_y is stored in heights.
                # To keep track of the decreasing velocities during the trajectory, the
                # velocities are stored and decreased in the v_x_drag, v_y_drag. If the
                # probe is in the target area, the velocity is added to the list of
                # velocities and the maximum of heights is stored in max_heights. If the
                # probe flew by the target area, the loop breaks and the next set of
                # (v_x, v_y) is tried out.
                s_x, s_y = (s_x + v_x_drag * step, s_y + v_y_drag * step)
                heights.add(s_y)

                if v_x_drag > 0:
                    v_x_drag += drag_x
                v_y_drag += drag_y

                if s_x > target_area_x[1] or s_y < target_area_y[0]:
                    break
                elif (
                    target_area_x[0] <= s_x <= target_area_x[1]
                    and target_area_y[0] <= s_y <= target_area_y[1]
                ):
                    max_heights.append(max(heights))
                    velocities.append((v_x, v_y))
                    break

    # Get the maximum height of all possible trajectories and the corresponding velocity.
    # Since both values are added two different lists at the same time, the indicies of
    # both values are identical.
    max_height = max(max_heights)
    velocity_max_height = velocities[max_heights.index(max(max_heights))]

    return velocities, velocity_max_height, max_height


if __name__ == "__main__":
    target_area = load_target_area("day_17_input.txt")
    velocities, velocity_max_height, max_height = find_highest_point(target_area)

    print(
        f"The maximum height possible is {max_height}"
        + f" with a velocity of {velocity_max_height}.\n"
        + f"The number possible velocities is: {len(velocities)}"
    )
