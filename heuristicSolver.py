import numpy as np
from solver import findCombinations
import math

def solvePuzzleHeuristic(w, h, y, x):
    grid = np.zeros((w, h))
    temp_grids = [np.copy(grid).tolist()]
    out_grid = []
    row_combinations = {}
    col_combinations = {}
    
    order = initRowColOrder(w,h,x,y)  
    
    while not np.array_equal(grid, out_grid):
        out_grid = np.copy(grid)
        for row_col in order:
            if row_col["axis"] == "row" and row_col["val"] < 16000:
                row = row_col["index"]
                # get possible row configurations
                if row_combinations.get(row) is None:
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
                                    updateRowColOrder(order, "row", col)

                            if append:
                                temp_grids.append(np.copy(grid).tolist())

            if row_col["axis"] == "col"  and row_col["val"] < 16000:
                col = row_col["index"]
                if col_combinations.get(col) is None:
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
    #                     print(combinations)
                        and_combinations = andCombinations(combinations)
    #                     print(and_combinations)
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
                                    updateRowColOrder(order, "col", row)

                            if append:
                                temp_grids.append(np.copy(grid).tolist())
            order.sort(key = lambda info: info["val"])

    grid = grid.tolist()
    return [grid, temp_grids]


def initRowColOrder(w, h, x, y):
    order = []
    for row in range(h):
        blocks = x[row]
        n_blocks = len(blocks)
        sum_blocks = np.sum(blocks)
        n_spaces = h - sum_blocks
        n_space_areas = n_blocks + 1
        n_free_spaces = n_spaces - n_space_areas + 2

        val = math.factorial(n_free_spaces + n_blocks)/(math.factorial(n_free_spaces) * math.factorial(n_blocks))
        order.append({
            "axis": "row",
            "index": row,
            "val": val,
            "n_free_spaces": n_free_spaces,
            "n_blocks": n_blocks
        })
    for col in range(w):
        blocks = y[col]
        n_blocks = len(blocks)
        sum_blocks = np.sum(blocks)
        n_spaces = w - sum_blocks
        n_space_areas = n_blocks + 1
        n_free_spaces = n_spaces - n_space_areas + 2

        val = math.factorial(n_free_spaces + n_blocks)/(math.factorial(n_free_spaces) * math.factorial(n_blocks))
        order.append({
            "axis": "col",
            "index": col,
            "val": val,
            "n_free_spaces": n_free_spaces,
            "n_blocks": n_blocks
        })
    order.sort(key = lambda info: info["val"])
    return order

# call when a square is ruled out
def updateRowColOrder(order, axis, index):
    for element in order:
        if axis == "col":
            desired_axis = "row"
        else:
            desired_axis = "col"
        if element["axis"] == desired_axis and element["index"] == index:
            element["n_free_spaces"] -= 1
            n_free_spaces = element["n_free_spaces"]
            n_blocks = element["n_blocks"]
            if n_free_spaces >= 0:
                val = math.factorial(n_free_spaces + n_blocks)/(math.factorial(n_free_spaces) * math.factorial(n_blocks))
                element["val"] = val
            break

def excludeCombinations(truth, combinations, length):
    indices = np.extract(truth != 0, np.arange(length))

    if indices.size == 0:
        return combinations
    else:
        truth_test = truth[indices] > 0
        bool_arr = [excludeCombination(truth_test, com, indices) for com in combinations]
        return np.compress(bool_arr, combinations, axis=0)


def excludeCombination(truth_test, combination, indices):
    combination_test = combination[indices]
    return np.all(
        np.logical_not(
            np.logical_xor(truth_test, combination_test)
        )
    )

def andCombinations(combinations):
    return np.logical_and.reduce(combinations)

def orCombinations(combinations):
    return np.logical_or.reduce(combinations)
