import os


#  Directions to check for adjacent risk levels
DIRECTIONS = [(0, 1), (1, 0)]


def load_risk_levels(file_name):
    # Create a list of each digit in the risk levels. Because the risk levels are 
    # given in one line as a coherent number, this number must be split in digits.
    split_num_into_digits = lambda num: [int(digit) for digit in str(num)]

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(file_path, "r", encoding="utf-8") as file_risk:
        risk_levels = [
            split_num_into_digits(line)
            for line in file_risk.read().split("\n")
        ]

    return risk_levels


def find_path_with_lowest_risk(risk_levels):
    possible_paths = [[[0,0]]]
    path = []
    paths = []
    total_risk = 0
    total_risks = []
    x_max = len(risk_levels[0]) - 1
    y_max = len(risk_levels) - 1
    
    while len(possible_paths) > 0:
        path = [risk_level for risk_level in possible_paths[0]]
        x = path[-1][0]
        y = path[-1][1]

        for dx, dy in DIRECTIONS:
            if 0 <= x + dx <= x_max and 0 <= y + dy <= y_max and [x+dx, y+dy] not in path and (x+dx, y+dy) != (x_max, y_max):
                print(path + [[x+dx,y+dy]])
                possible_paths.append(path + [[x+dx, y+dy]])
            elif (x+dx, y+dy) == (x_max, y_max):
                print(paths+ [[x+dx,y+dy]])
                paths.append(path + [[x+dx,y+dy]])

        possible_paths = possible_paths[1:]

    for path in paths:
        total_risk = 0
        print("path: ", path)
        for x,y in path:
            print(x,y)
            total_risk += risk_levels[y][x]
        
        total_risks.append(total_risk-risk_levels[0][0])

    return min(total_risks)


if __name__ == "__main__":
    risk_levels = load_risk_levels("day_15_example_input.txt")
    for line in risk_levels:
        print(line)

    lowest_risk = find_path_with_lowest_risk(risk_levels)
    print(lowest_risk)