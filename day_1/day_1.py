import numpy as np
from pathlib import Path


def increase(depths):
    counter = 0
    for i in range(len(depths)-1):
        if depths[i+1] > depths[i]:
            counter += 1
    return counter


example_list = [
    199, 200, 208,
    210, 200, 207,
    240, 269, 260,
    263
]

p = Path(__file__).with_name('day_1_input.txt')

with p.open('rb') as file:
    measurements = np.loadtxt(file)

print(f'The number of times a depth measurement increases is: {increase(measurements)}')
