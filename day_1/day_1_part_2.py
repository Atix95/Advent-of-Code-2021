import numpy as np
from pathlib import Path


def increase(sum_of_depths):
    counter = 0
    for i in range(len(sum_of_depths)-1):
        if sum_of_depths[i+1] > sum_of_depths[i]:
            counter += 1
    return counter


def sum_of_list(depths):
    sum_of_depths = [0]*(len(depths)-2)
    for i in range(len(depths)-2):
        sum_of_depths[i] = depths[i] + depths[i+1] + depths[i+2]
    return sum_of_depths


example_list = [
    199, 200, 208,
    210, 200, 207,
    240, 269, 260,
    263
]

p = Path(__file__).with_name('day_1_input.txt')

with p.open('rb') as file:
    measurements = np.loadtxt(file)

print(f'The number of times a depth measurement increases is: {increase(sum_of_list(measurements))}')
