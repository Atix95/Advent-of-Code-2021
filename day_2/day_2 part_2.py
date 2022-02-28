# Second advent of code exercise by Atix95.
# The code is written to get the job done,
# which is why it might not be optimally written.


from pathlib import Path


def piloting(commands):
    horizontal = 0
    depth = 0
    aim = 0

    for i in range(len(commands)):
        commands[i] = commands[i].strip()
        if commands[i][:-1] == 'forward ':
            horizontal += int(commands[i][-1])
            depth += aim*int(commands[i][-1])
        elif commands[i][:-1] == 'up ':
            aim -= int(commands[i][-1])
        elif commands[i][:-1] == 'down ':
            aim += int(commands[i][-1])

    return depth*horizontal


example_log = [
    'forward 5',
    'down 5',
    'forward 8',
    'up 3',
    'down 8',
    'forward 2'
]

p = Path(__file__).with_name('day_2_input.txt')

with p.open('r', encoding='utf-8') as file:
    piloting_log = file.readlines()

print(f'The product of the final depth and horizontal position is: {piloting(piloting_log)}')