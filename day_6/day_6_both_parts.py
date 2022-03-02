import os


DAYS_TILL_REPRODUCTION = 9


def load_initial_lanternfish(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_fishes:
        initial_lanternfish = [
            int(lanternfish) for lanternfish in file_fishes.read().strip().split(",")
        ]

    return initial_lanternfish


def create_initial_state(initial_lanternfish):
    initial_state = []

    for internal_timer in range(DAYS_TILL_REPRODUCTION):
        initial_state.append(initial_lanternfish.count(internal_timer))

    return initial_state


def lanternfish_reproduction(initial_state, days):
    lanternfish_state = create_initial_state(initial_state)

    for day in range(days):
        lanternfish_state = lanternfish_state[1:] + lanternfish_state[:1]
        lanternfish_state[DAYS_TILL_REPRODUCTION - 3] += lanternfish_state[-1]

    return lanternfish_state


if __name__ == "__main__":
    days = 256

    final_state_lanternfish = lanternfish_reproduction(
        load_initial_lanternfish("day_6_input.txt"), days
    )

    print(
        f"The final state of the lanternfish population is:\n{final_state_lanternfish}\n"
        + f"The size of the population is: {sum(final_state_lanternfish)}"
    )

