# Third advent of code exercise by Atix95.
# The code is written to get the job done,
# which is why it might not be optimally written.


from pathlib import Path


def oxygen_generator_rating(binary_numbers):
    digits = len(binary_numbers[0])
    
    for j in range(digits):
        zeros = 0
        ones = 0
        zero_numbers = []
        one_numbers = []

        for i in range(len(binary_numbers)):
            if binary_numbers[i][j] == '0':
                zeros += 1
                zero_numbers.append(binary_numbers[i])
            else:
                ones += 1
                one_numbers.append(binary_numbers[i])

        if len(zero_numbers) <= 1 and len(one_numbers) <= 1:
            break
        if len(zero_numbers) <= len(one_numbers):
            binary_numbers = one_numbers
        else:
            binary_numbers = zero_numbers

    return int(one_numbers[0], 2)


def co2_scrubber_rating(binary_numbers):
    digits = len(binary_numbers[0])

    for j in range(digits):
        zeros = 0
        ones = 0
        zero_numbers = []
        one_numbers = []

        for i in range(len(binary_numbers)):
            if binary_numbers[i][j] == '0':
                zeros += 1
                zero_numbers.append(binary_numbers[i])
            else:
                ones += 1
                one_numbers.append(binary_numbers[i])

        if len(zero_numbers) <= 1 and len(one_numbers) <= 1:
            break
        if len(zero_numbers) <= len(one_numbers):
            binary_numbers = zero_numbers
        else:
            binary_numbers = one_numbers

    return int(zero_numbers[0], 2)



example_binaries = [
    '00100', '11110', '10110',
    '10111', '10101', '01111',
    '00111', '11100', '10000',
    '11001', '00010', '01010'
]

p = Path(__file__).with_name('day_3_input.txt')

with p.open('r', encoding='utf-8') as file:
    diagnostic_report = [i for i in file.read().strip().split('\n')]

print(
    'The life support rating of the submarine is:',
    oxygen_generator_rating(diagnostic_report) * co2_scrubber_rating(diagnostic_report)
)