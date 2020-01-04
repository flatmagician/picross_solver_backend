import numpy as np
from solver import findCombinations


def solvePuzzleHeuristic(w, h, y, x):
    grid = np.zeros((w, h))
    temp_grids = [np.copy(grid).tolist()]
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

            if type(combinations) is not str:
                current_row = grid[row, :]
                # exclude configurations that conflict with truth
                combinations = excludeCombinations(current_row, combinations, h)
                # store valid configurations
                if len(combinations) == 1:
                    row_combinations[row] = "complete"
                    for col in range(w):
                        if combinations[0][col] == 1:
                            grid[row, col] = 1
                        else:
                            grid[row, col] = -2
                    temp_grids.append(np.copy(grid).tolist())
                else:
                    row_combinations[row] = combinations

                    and_combinations = andCombinations(combinations)
                    or_combinations = orCombinations(combinations)
                    for col in range(w):
                        append = False

                        val = and_combinations[col]
                        if val == True:
                            if grid[row, col] != 1:
                                grid[row, col] = 1
                                append = True

                        val = or_combinations[col]
                        if val == False:
                            if grid[row, col] != -2:
                                grid[row, col] = -2
                                append = True

                        if append:
                            temp_grids.append(np.copy(grid).tolist())

        for col in range(w):
            if not col_combinations.get(col):
                combinations = findCombinations(y[col], h)
                col_combinations[col] = combinations
            else:
                combinations = col_combinations[col]
            
            if type(combinations) is not str:
                current_col = grid[:, col]
                combinations = excludeCombinations(current_col, combinations, h)
                if len(combinations) == 1:
                    col_combinations[col] = "complete"
                    for row in range(h):
                        if combinations[0][row] == 1:
                            grid[row, col] = 1
                        else:
                            grid[row, col] = -2
                    temp_grids.append(np.copy(grid).tolist())
                else:
                    col_combinations[col] = combinations
                    print(combinations)
                    and_combinations = andCombinations(combinations)
                    print(and_combinations)
                    or_combinations = orCombinations(combinations)
                    for row in range(h):
                        append = False

                        val = and_combinations[row]
                        if val == True:
                            if grid[row, col] != 1:
                                grid[row, col] = 1
                                append = True

                        val = or_combinations[row]
                        if val == False:
                            if grid[row, col] != -2:
                                grid[row, col] = -2
                                append = True

                        if append:
                            temp_grids.append(np.copy(grid).tolist())

    grid = grid.tolist()
    return [grid, temp_grids]


def excludeCombinations(truth, combinations, length):
    out_combinations = []
    for combination in combinations:
        to_include = True
        for i in range(length):
            if truth[i] == 1 and combination[i] == 0:
                to_include = False
                break
            if truth[i] < 0 and combination[i] == 1:
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
