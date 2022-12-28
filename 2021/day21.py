import time

import numpy as np
from joblib import Parallel, delayed

dirac_dice_rolls = (3, 4, 5, 6, 7, 8, 9)
dirac_dice_rolls_count = (1, 3, 6, 7, 6, 3, 1)


class DeterministicDice:
    def __init__(self):
        self.next_roll = 1
        self.count = 0

    def roll(self) -> int:
        self.count += 1
        this_roll = self.next_roll
        self.next_roll = self.next_roll % 100 + 1
        return this_roll

    def triple_roll(self) -> int:
        return sum([self.roll() for _ in range(3)])


def dirac_game(positions, points, player):
    wins = np.array([0, 0])
    if np.any(points >= 21):
        winner = np.argmin(points)
        wins[winner] = 1

        return wins

    for triple_roll, count in zip(dirac_dice_rolls, dirac_dice_rolls_count):
        new_pos = positions.copy()
        new_points = points.copy()
        new_pos[player] = (new_pos[player] + triple_roll - 1) % 10 + 1
        new_points[player] += new_pos[player]
        next_player = 0 if player == 1 else 1
        inner_wins = dirac_game(new_pos, new_points,  player=next_player)
        wins += count * inner_wins

    return wins


def parallell_helper(starting_point, triple_roll, count):
    player = 0
    new_pos = starting_point.copy()
    new_points = np.array([0, 0])
    new_pos[player] = (new_pos[player] + triple_roll - 1) % 10 + 1
    new_points[player] += new_pos[player]
    next_player = 0 if player == 1 else 1
    inner_wins = dirac_game(new_pos, new_points,  player=next_player)
    return count * inner_wins


# a
positions = np.array([9, 3])
points = np.array([0, 0])
dice = DeterministicDice()

while not np.any(points >= 1000):
    for player in range(len(positions)):
        new_pos = (positions[player] + dice.triple_roll() - 1) % 10 + 1
        positions[player] = new_pos
        points[player] += new_pos
        if np.any(points >= 1000):
            break
print(np.min(points) * dice.count)


# b
t0 = time.time()

starting_point = np.array([9, 3])
values = Parallel(n_jobs=7, backend='multiprocessing')(delayed(parallell_helper)(
    starting_point, triple_roll, count) for triple_roll, count in zip(dirac_dice_rolls, dirac_dice_rolls_count))
all_points = np.stack(values).sum(axis=0)

t1 = time.time()
time_elapsed = t1-t0

print(np.max(all_points))
print(f'Running time {time_elapsed/60} minutes')
