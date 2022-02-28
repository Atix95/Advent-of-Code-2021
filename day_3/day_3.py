# Third advent of code exercise by Atix95.
# The code is written to get the job done,
# which is why it might not be optimally written.


from pathlib import Path


def power_consumption(binary_numbers):
    digits = len(binary_numbers[0])
    ones = [0]*digits
    zeros = [0]*digits
    gamma_rate = ''
    epsilon_rate = ''

    for i in range(len(binary_numbers)):        
        for j in range(digits):
            if binary_numbers[i][j] == '0':
                zeros[j] += 1
            else:
                ones[j] += 1
    
    for i in range(digits):
        if zeros[i] < ones[i]:
            gamma_rate += '1'
            epsilon_rate += '0'
        else:
            gamma_rate += '0'
            epsilon_rate += '1'

    return int(gamma_rate, 2)*int(epsilon_rate, 2)


example_binaries = [
    '00100', '11110', '10110',
    '10111', '10101', '01111',
    '00111', '11100', '10000',
    '11001', '00010', '01010'
]


p = Path(__file__).with_name('day_3_input.txt')

with p.open('r', encoding='utf-8') as file:
    diagnostic_report = [i for i in file.read().strip().split('\n')]

print(f'The power consumption of the submarine is: {power_consumption(diagnostic_report)}')