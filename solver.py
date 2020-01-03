import numpy as np
import matplotlib.pyplot as plt
from sympy.utilities.iterables import multiset_permutations

# can only pass valid combinations to this function


def findCombinations(blocks, length):
    n_blocks = len(blocks)
    sum_blocks = np.sum(blocks).astype(np.uint8)
    n_spaces = length - sum_blocks
    n_space_areas = n_blocks + 1
    n_free_spaces = n_spaces - n_space_areas + 2

    space_positions = ["s" for i in range(n_free_spaces)]
    block_positions = ["b" for i in range(n_blocks)]
    space_array = space_positions + block_positions
    combinations = multiset_permutations(space_array)
    result = [constructRow(combination, blocks, n_blocks, length)
              for combination in combinations]
    return result


def constructRow(combination, blocks, n_blocks, length):
    row = np.zeros(length)
    block_count = 0
    index = 0
    for char in combination:
        if char == "s":
            index += 1
        if char == "b":
            block_length = blocks[block_count]
            for i in range(block_length):
                row[index] = 1
                index += 1
            block_count += 1
            if block_count != n_blocks:
                index += 1
    return row


# def solvePuzzle(w, h, x, y, row_index, puzzle):
#     if row_index == h:
#         return puzzle
#     ind = 0
#     combinations = findCombinations(y[row_index], w)
#     for combination in combinations:
#         if row_index == 0:
#             temp_puzzle = combination
#             ind += 1
#         else:
#             temp_puzzle = np.vstack([puzzle, combination])
#         if checkPuzzle(temp_puzzle, x, row_index, False):
#             out_puzzle = solvePuzzle(w, h, x, y, row_index+1, temp_puzzle)
#             if np.shape(out_puzzle) == (w, h):
#                 if checkPuzzle(out_puzzle, x, row_index, True):
#                     return out_puzzle
def solvePuzzle(w, h, x, y, row_index, puzzle, temp_puzzles):
    if row_index == h:
        return puzzle
    ind = 0
    combinations = findCombinations(y[row_index], w)
    for combination in combinations:
        if row_index == 0:
            temp_puzzle = combination
            ind += 1
        else:
            temp_puzzle = np.vstack([puzzle, combination])
        temp_puzzles.append(temp_puzzle)
        if checkPuzzle(temp_puzzle, x, row_index, False):
            out_puzzle = solvePuzzle(
                w, h, x, y, row_index+1, temp_puzzle, temp_puzzles)
            if np.shape(out_puzzle) == (w, h):
                if checkPuzzle(out_puzzle, x, row_index, True):
                    return out_puzzle


def checkPuzzle(temp_puzzle, x, row_index, final):
    if row_index == 0:
        return True
    for i in range(len(x)):
        col = temp_puzzle[:, i]
        if not checkCol(col, x[i], final):
            return False
    return True


def checkCol(column, block_info, final):
    # check for too few in a row
    n_blocks = len(block_info)
    block_count = 0
    block_len = 0
    prev_entry = 0
    for entry in column:
        if block_count > n_blocks:
            return False
        elif block_count < n_blocks:
            if block_len > block_info[block_count]:
                return False
        else:
            if block_len > 0:
                return False

        if entry == 0 and prev_entry == 0:
            block_len = 0
        if entry == 1 and prev_entry == 0:
            block_len += 1
        if entry == 0 and prev_entry == 1:
            if block_len < block_info[block_count]:
                return False
            block_len = 0
            block_count += 1
        if entry == 1 and prev_entry == 1:
            block_len += 1

        prev_entry = entry
    if final:
        if prev_entry == 1:
            block_count += 1
            if block_len != block_info[n_blocks - 1]:
                return False
        if block_count != n_blocks:
            return False
    return True
    # check for too many in a row


def solverWrapper(w, h, x, y, row_index, puzzle):
    temp_puzzles = []
    puzzle = solvePuzzle(w, h, x, y, 0, None, temp_puzzles)
    return puzzle, temp_puzzles
