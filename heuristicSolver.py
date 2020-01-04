import numpy as np
from solver import findCombinations


def solvePuzzleHeuristic(w, h, y, x):
    grid = np.zeros((w, h))
    temp_grids = [np.copy(grid)]
    out_grid = []
    row_combinations = {}
    col_combinations = {}
    while not np.array_equal(grid, out_grid):
        out_grid = np.copy(grid)
        for row in range(h):
            # get possible row configurations
            if not row_combinations.get(row):
                combinations = findCombinations(x[row], w)
                row_combinations[row] = combinations
            else:
                combinations = row_combinations[row]
            # get current row truth
            current_row = grid[row, :]
            # exclude configurations that conflict with truth
            combinations = excludeCombinations(current_row, combinations, h)
            # store valid configurations
            row_combinations[row] = combinations

            and_combinations = andCombinations(combinations)
            or_combinations = orCombinations(combinations)
            for col in range(w):
                append = False

                val = and_combinations[col]
                if val == True:
                    grid[row, col] = 1
                    append = True

                val = or_combinations[col]
                if val == False:
                    grid[row, col] = -1
                    append = True

                if append:
                    temp_grids.append(np.copy(grid))

        for col in range(w):
            if not col_combinations.get(row):
                combinations = findCombinations(y[col], h)
                col_combinations[row] = combinations
            else:
                combinations = col_combinations[row]

            current_col = grid[:, col]
            combinations = excludeCombinations(current_col, combinations, h)
            col_combinations[row] = combinations

            and_combinations = andCombinations(combinations)
            or_combinations = orCombinations(combinations)
            for row in range(h):
                append = False

                val = and_combinations[row]
                if val == True:
                    grid[row, col] = 1

                val = or_combinations[row]
                if val == False:
                    grid[row, col] = -1

                if append:
                    temp_grids.append(np.copy(grid))

    for i in range(len(temp_grids)):
        temp_grids[i] = temp_grids[i].tolist()
    for temp_grid in temp_grids:
        for row in range(h):
            for col in range(w):
                val = temp_grid[row][col]
                if val == -1:
                    temp_grid[row][col] = -2
    grid = grid.tolist()
    for row in range(h):
        for col in range(w):
            val = grid[row][col]
            if val == -1:
                grid[row][col] = 0
    return [grid, temp_grids]


def excludeCombinations(truth, combinations, length):
    out_combinations = []
    for combination in combinations:
        to_include = True
        for i in range(length):
            if truth[i] == 1 and combination[i] == 0:
                to_include = False
                break
            if truth[i] == -1 and combination[i] == 1:
                to_include = False
                break
        if to_include:
            out_combinations.append(combination)
    return out_combinations


def andCombinations(combinations):
    if len(np.shape(combinations)) == 1:
        return combinations
    combination = combinations[0]
    for new_combination in combinations[1:]:
        combination = np.logical_and(combination, new_combination)
    return combination


def orCombinations(combinations):
    if len(np.shape(combinations)) == 1:
        return combinations
    combination = combinations[0]
    for new_combination in combinations[1:]:
        combination = np.logical_or(combination, new_combination)
    return combination
