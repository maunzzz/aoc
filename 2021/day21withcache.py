import time

from functools import cache

dirac_dice_rolls = (3, 4, 5, 6, 7, 8, 9)
dirac_dice_rolls_count = (1, 3, 6, 7, 6, 3, 1)


@cache
def dirac_game(pos1, pos2, points1, points2, player):
    if points1 >= 21:
        return (1, 0)
    elif points2 >= 21:
        return (0, 1)

    wins = (0, 0)
    for triple_roll, count in zip(dirac_dice_rolls, dirac_dice_rolls_count):
        new_pos = [pos1, pos2]
        new_points = [points1, points2]

        new_pos[player] = (new_pos[player] + triple_roll - 1) % 10 + 1
        new_points[player] += new_pos[player]
        next_player = 0 if player == 1 else 1
        inner_wins = dirac_game(new_pos[0], new_pos[1], new_points[0], new_points[1],  player=next_player)
        wins = (wins[0] + count * inner_wins[0], wins[1] + count * inner_wins[1])

    return wins


t0 = time.time()

wins = dirac_game(9, 3, 0, 0, 0)

t1 = time.time()
time_elapsed = t1-t0

print(max(wins))
print(f'Running time {time_elapsed} seconds')
