import re

import numpy as np

exp = re.compile(f"(on|off) x=([\d-]+)\.\.([\d-]+),y=([\d-]+)\.\.([\d-]+),z=([\d-]+)\.\.([\d-]+)")
instructions = []
with open('inputs/day22') as f:
    for line in f:
        mat = exp.match(line)
        edges = [int(g) for g in mat.groups()[1:]]
        instructions.append((mat.groups()[0] == 'on', edges))

x_vals = list()
y_vals = list()
z_vals = list()

for instruction in instructions:
    x_vals.extend([instruction[1][0], instruction[1][1]+1])
    y_vals.extend([instruction[1][2], instruction[1][3]+1])
    z_vals.extend([instruction[1][4], instruction[1][5]+1])

x_vals = np.unique(x_vals)
y_vals = np.unique(y_vals)
z_vals = np.unique(z_vals)

shape = np.array([len(x_vals), len(y_vals), len(z_vals)])
tile_volumes = np.ones(shape - 1, dtype=np.int32)*np.diff(x_vals)[:, np.newaxis, np.newaxis] * \
    np.ones(shape - 1, dtype=np.int32)*np.diff(y_vals)[np.newaxis, :, np.newaxis] * \
    np.ones(shape - 1, dtype=np.int32)*np.diff(z_vals)[np.newaxis, np.newaxis, :]
cube_vol = np.zeros(shape-1, dtype=bool)

x_val_to_index = {val: i for i, val in enumerate(x_vals)}
y_val_to_index = {val: i for i, val in enumerate(y_vals)}
z_val_to_index = {val: i for i, val in enumerate(z_vals)}

for i, instruction in enumerate(instructions):
    start = [x_val_to_index[instruction[1][0]], y_val_to_index[instruction[1][2]], z_val_to_index[instruction[1][4]]]
    stop = [x_val_to_index[instruction[1][1]+1], y_val_to_index[instruction[1][3]+1],
            z_val_to_index[instruction[1][5]+1]]
    cube_vol[start[0]:stop[0], start[1]:stop[1], start[2]:stop[2]] = instruction[0]
    if i == 19:
        print(np.sum(cube_vol*tile_volumes))

print(np.sum(cube_vol*tile_volumes))
