
import numpy as np

with open('2021/inputs/day25') as f:
    lines = f.read().splitlines()

lookup = {'.': 0, '>': 1, 'v': 2}

cucumber_map = np.stack([np.array([lookup[ch] for ch in line]) for line in lines])

any_moves = True
count = 0
while any_moves:
    any_moves = False

    east_starts = np.argwhere(cucumber_map == 1)
    east_stops = []
    for es in east_starts:
        stop = (es[0], (es[1] + 1) % cucumber_map.shape[1])
        if cucumber_map[stop] != 0:
            east_stops.append(None)
        else:
            east_stops.append(stop)
            any_moves = True

    for start, stop in zip(east_starts, east_stops):
        if stop is not None:
            cucumber_map[tuple(start)] = 0
            cucumber_map[stop] = 1

    south_starts = np.argwhere(cucumber_map == 2)
    south_stops = []
    for ss in south_starts:
        stop = ((ss[0] + 1) % cucumber_map.shape[0], ss[1])
        if cucumber_map[stop] != 0:
            south_stops.append(None)
        else:
            south_stops.append(stop)
            any_moves = True

    for start, stop in zip(south_starts, south_stops):
        if stop is not None:
            cucumber_map[tuple(start)] = 0
            cucumber_map[stop] = 2
    count += 1

print(count)
