
from itertools import product

instructions = []
with open('2021/inputs/day24') as f:
    for line in f:
        instructions.append(line.rstrip())

# save values that differ for instructions
v1s, v2s, divs = [], [], []
for i in range(0, len(instructions), 18):
    v1s.append(int(instructions[i + 5].split()[-1]))
    v2s.append(int(instructions[i + 15].split()[-1]))
    divs.append(int(instructions[i + 4].split()[-1]))


def run_alu_symb():  # used to figure out pattern between inputs
    input_index = 0

    variable_dict = dict()

    for instruction in instructions:

        ins = instruction.split()
        if ins[0] == 'inp':
            # variable_dict[ins[1]] = f'input{input_index}'
            variable_dict['x'] = f'x{input_index}'
            variable_dict['y'] = f'y{input_index}'
            variable_dict['z'] = f'z{input_index}'
            variable_dict['w'] = f'w{input_index}'
            input_index += 1
        else:
            if ins[2] in {'x', 'y', 'z', 'w'}:
                num2 = variable_dict[ins[2]]
            else:
                num2 = ins[2]

            if ins[0] == 'add':
                if variable_dict[ins[1]] == '0':
                    variable_dict[ins[1]] = num2
                else:
                    variable_dict[ins[1]] = f'({variable_dict[ins[1]]} + {num2})'
            elif ins[0] == 'sub' and num2 != '0':
                variable_dict[ins[1]] = f'({variable_dict[ins[1]]} - {num2})'
            elif ins[0] == 'mul':
                if num2 == '0':
                    variable_dict[ins[1]] = '0'
                else:
                    variable_dict[ins[1]] = f'({variable_dict[ins[1]]} * {num2})'
            elif ins[0] == 'div':
                variable_dict[ins[1]] = f'({variable_dict[ins[1]]} // {num2})'
            elif ins[0] == 'mod':
                variable_dict[ins[1]] = f'({variable_dict[ins[1]]} % {num2})'
            elif ins[0] == 'eql':
                variable_dict[ins[1]] = f'({variable_dict[ins[1]]} == {num2})'

    return variable_dict['z']


def run_alu(input):  # brute force run, used for debugging only
    input_index = 0

    variable_dict = dict()
    variable_dict['x'] = 0
    variable_dict['y'] = 0
    variable_dict['z'] = 0
    variable_dict['w'] = 0

    for instruction in instructions:
        ins = instruction.split()
        if ins[0] == 'inp':
            variable_dict[ins[1]] = input[input_index]
            input_index += 1
        else:
            if ins[2] in {'x', 'y', 'z', 'w'}:
                num2 = variable_dict[ins[2]]
            else:
                num2 = int(ins[2])

            if ins[0] == 'add':
                variable_dict[ins[1]] = variable_dict[ins[1]] + num2
            elif ins[0] == 'sub':
                variable_dict[ins[1]] = variable_dict[ins[1]] - num2
            elif ins[0] == 'mul':
                variable_dict[ins[1]] = variable_dict[ins[1]] * num2
            elif ins[0] == 'div':
                variable_dict[ins[1]] = variable_dict[ins[1]] // num2
            elif ins[0] == 'mod':
                variable_dict[ins[1]] = variable_dict[ins[1]] % num2
            elif ins[0] == 'eql':
                variable_dict[ins[1]] = (variable_dict[ins[1]] == num2)

    return variable_dict['z']


def run_alu_simplified(inputs):
    # the alu creates a repeating pattern for each input digit, use run_alu_symb to see this pattern
    # x[n+1] = ((z[n] % 26 + v1[n]) == input[n]) == 0
    # z[n+1] = (z[n] // divs[n]) * (25 * x[n+1] + 1) + input[0] + v2[n] * x[n+1]
    # v1,v2 and divs are values that differ for each period
    # Looking at these numbers we realize that x[n+1] only can be zero when v1[n] is negative
    # z[n+1] is increasing and can only decrease when divs[n] != 1 (divs are 1 or 26)
    # idea: when v1[n] is negative, set inputs[n] such that x[n+1] == 0 (keep z[n+1] low).
    # This decreases the number of inputs needed to be checked from 9^14 to 9^7
    x = 0
    z = 0
    model_nr = []
    for i, input in enumerate(inputs):
        if input is None:
            wanted_value = z % 26 + v1s[i]
            if wanted_value > 0 and wanted_value < 10:
                input = wanted_value
            else:
                input = 9

        x = ((z % 26 + v1s[i]) == input) == 0
        z = (z // divs[i]) * (25*x+1) + (input + v2s[i]) * x
        model_nr.append(input)
    return z, model_nr


def find_number(find_largest: bool):
    model_nr = 14*[None]
    indices_to_iterate_over = [i for i, n in enumerate(v1s) if n > 0]

    start, stop, inc = (9, 0, -1) if find_largest else (1, 10, 1)
    for nums in product(range(start, stop, inc), repeat=7):
        for i, num in enumerate(nums):
            model_nr[indices_to_iterate_over[i]] = num
        z_val, model_nr_used = run_alu_simplified(model_nr)
        if z_val == 0:
            return model_nr_used


print(''.join(str(n) for n in find_number(True)))
print(''.join(str(n) for n in find_number(False)))
