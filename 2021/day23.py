from copy import deepcopy
from queue import PriorityQueue

import numpy as np


class AmphipodMover:
    def __init__(self, mode):
        self.row = np.zeros((11,), dtype=np.int32)
        if mode == 'example':
            self.holes = np.array([[2, 1], [3, 4], [2, 3], [4, 1]], dtype=np.int32)
        elif mode == 'a':
            self.holes = np.array([[4, 3], [3, 4], [1, 1], [2, 2]], dtype=np.int32)
        elif mode == 'b':
            self.holes = np.array([[4, 4, 4, 3], [3, 3, 2, 4], [1, 2, 1, 1], [2, 1, 3, 2]], dtype=np.int32)

        self.hole_positions = np.array([2, 4, 6, 8], dtype=np.int32)
        self.cost = 0

    def key(self):
        chars = []
        chars.extend([str(num) for num in self.holes.flatten()])
        chars.extend([str(num) for num in self.row])
        return '-'.join(ch for ch in chars)

    def move(self, hole_index, row_position, out_of_hole):
        assert np.all(self.holes[hole_index[0], 0:hole_index[1]] == 0)

        hole_pos = self.hole_positions[hole_index[0]]
        lower_pos = min(hole_pos, row_position)
        higher_pos = max(hole_pos, row_position)

        if out_of_hole:
            index_moved = self.holes[hole_index[0], hole_index[1]]
        else:
            index_moved = self.row[row_position]

        cost_multiplier = 10 ** (index_moved - 1)
        moved_length = higher_pos-lower_pos+1+hole_index[1]

        self.cost += moved_length * cost_multiplier

        # change positions
        if out_of_hole:
            self.row[row_position] = index_moved
            self.holes[hole_index[0], hole_index[1]] = 0
        else:
            self.row[row_position] = 0
            self.holes[hole_index[0], hole_index[1]] = index_moved

    def done(self):
        for i in range(4):
            if np.any(self.holes[i] != i+1):
                return False
        return True

    def get_valid_next_moves(self):
        valid_moves = []
        if self.done():
            return valid_moves

        for row_index in range(11):  # corridor to holes
            amphipod_type = self.row[row_index]
            if amphipod_type != 0:
                hole_index = amphipod_type - 1
                hole = self.holes[hole_index]
                hole_pos = self.hole_positions[hole_index]

                # no other types
                if np.any(hole[hole > 0] != amphipod_type):
                    continue

                # check if path is blocked
                blocked = True
                if row_index < hole_pos:
                    if np.all(self.row[row_index+1:hole_pos] == 0):
                        blocked = False
                else:
                    if np.all(self.row[hole_pos:row_index] == 0):
                        blocked = False

                # check which position to move into
                if not blocked:
                    hole_depth = len(hole) - 1
                    while hole_depth >= 0 and hole[hole_depth] != 0:
                        hole_depth -= 1
                    if hole_depth == -1:  # full
                        continue
                    valid_moves.append(([hole_index, hole_depth], row_index, False))
                    return valid_moves  # if we can move to final position, this is the best current move

        for hole_index, hole in enumerate(self.holes):  # top amphi can move to any valid row pos that is not blocked
            hole_depth = 0
            while hole_depth < len(hole) and hole[hole_depth] == 0:
                hole_depth += 1
            if hole_depth == len(hole):  # empty
                continue

            if np.all(hole[1:] == hole_index + 1):  # already at right place
                continue

            hole_pos = self.hole_positions[hole_index]
            for row_index in range(11):
                if row_index in self.hole_positions:
                    continue
                if row_index < hole_pos:
                    if np.all(self.row[row_index:hole_pos] == 0):
                        valid_moves.append(([hole_index, hole_depth], row_index, True))
                else:
                    if np.all(self.row[hole_pos:row_index+1] == 0):
                        valid_moves.append(([hole_index, hole_depth], row_index, True))

        return valid_moves

    def __lt__(self, other):
        return self.cost < other.cost


def find_optimal_movement(mode):
    movers_queue = PriorityQueue()
    start = AmphipodMover(mode=mode)
    movers_queue.put(start)

    visited = set()
    count = 0
    while movers_queue:
        this = movers_queue.get(block=False)
        if count % 10000 == 0:
            print(f'{this.cost} - {movers_queue.qsize()} - {len(visited)}')
        count += 1

        if this.done():
            return this.cost

        this_key = this.key()
        if this_key in visited:  # no need to add visited states since previous costs are lower
            continue

        visited.add(this_key)
        for next_move in this.get_valid_next_moves():
            next = deepcopy(this)
            next.move(*next_move)
            movers_queue.put(next)


if __name__ == '__main__':
    print(find_optimal_movement('a'))
    print(find_optimal_movement('b'))
