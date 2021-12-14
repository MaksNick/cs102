from copy import deepcopy
from random import choice, randint, seed
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    lny = len(grid[0])
    x = coord[0]
    y = coord[1]
    num = choice((0, 1))
    if x - 1 != 0 and y + 1 != lny - 1 and num == 1 or x - 1 == 0 and y + 1 != lny - 1:
        grid[x][y + 1] = " "
    elif x - 1 != 0 and y + 1 != lny - 1 and num == 0 or x - 1 != 0 and y + 1 == lny - 1:
        grid[x - 1][y] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for i, cell in enumerate(empty_cells):
        remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    coord = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "X":
                coord.append((x, y))
    return coord


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == k and grid[i][j] == 1:
                if i == 0:
                    grid[i + 1][j] = k + 1
                if i == len(grid) - 1:
                    grid[i - 1][j] = k + 1
                if j == 0:
                    grid[i][j + 1] = k + 1
                if j == len(grid[0]) - 1:
                    grid[i][j - 1] = k + 1
            elif grid[i][j] == k:
                if grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1
    return grid


def shortest_path(grid, exit_coord: Tuple[int, int]) -> List[Tuple[int, ...]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    path = []
    path.append(tuple([exit_coord[0], exit_coord[1]]))
    k = grid[exit_coord[0]][exit_coord[1]]
    i = exit_coord[0]
    j = exit_coord[1]
    if grid[i][j] == k:
        if j - 1 >= 0 and j + 1 <= len(grid[0]) - 1:
            if grid[i][j - 1] == 1:
                path.append(tuple([i, j - 1]))
                return path
            if grid[i][j + 1] == 1:
                path.append(tuple([i, j + 1]))
                return path
        if i - 1 >= 0 and i + 1 <= len(grid) - 1:
            if grid[i - 1][j] == 1:
                path.append(tuple([i - 1, j]))
                return path
            if grid[i + 1][j] == 1:
                path.append(tuple([i + 1, j]))
                return path
    while k != 1:
        if grid[i][j] == k:
            if grid[i - 1][j] == k - 1:
                k -= 1
                i, j = i - 1, j
                path.append(tuple([i, j]))
            elif grid[i + 1][j] == k - 1:
                k -= 1
                i, j = i + 1, j
                path.append(tuple([i, j]))
            elif grid[i][j - 1] == k - 1:
                k -= 1
                i, j = i, j - 1
                path.append(tuple([i, j]))
            elif grid[i][j + 1] == k - 1:
                k -= 1
                i, j = i, j + 1
                path.append(tuple([i, j]))
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """
    lnx = len(grid)
    lny = len(grid[0])
    if (
        coord[0] == lnx - 1
        and coord[1] == lny - 1
        or coord[0] == 0
        and coord[1] == 0
        or coord[0] == lnx - 1
        and coord[1] == 0
        or coord[0] == 0
        and coord[1] == lny - 1
    ):
        return True
    if coord[0] == 1 and coord[1] == 0 or coord[0] == 0 and coord[1] == 1:
        if grid[2][1] != " " and grid[1][2] != " " and grid[1][1] != " ":
            return True
    if coord[0] == 0 and coord[1] == lny - 2 or coord[0] == 1 and coord[1] == lny - 1:
        if grid[1][lny - 3] != " " and grid[2][lny - 2] != " " and grid[1][lny - 2] != " ":
            return True
    if coord[0] == lnx - 1 and coord[1] == 1 or coord[0] == lnx - 2 and coord[1] == 0:
        if grid[lnx - 3][1] != " " and grid[lnx - 2][2] != " " and grid[lnx - 2][1] != " ":
            return True
    if coord[0] == lnx - 1 and coord[1] == lny - 2 or coord[0] == lnx - 2 and coord[1] == lny - 1:
        if (
            grid[lnx - 1][lny - 3] != " "
            and grid[lnx - 3][lny - 2] != " "
            and grid[lnx - 2][lny - 2] != " "
        ):
            return True
    if coord[0] == 0 and grid[1][coord[1]] != " ":
        return True
    if coord[0] == lnx - 1 and grid[lnx - 2][coord[1]] != " ":
        return True
    if coord[1] == 0 and grid[coord[0]][1] != " ":
        return True
    if coord[1] == lny - 1 and grid[coord[0]][lny - 2] != " ":
        return True
    return False


def solve_maze(grid: List[List[Union[str, int]]]):
    """
    :param grid:
    :return:
    """
    lnx = len(grid)
    lny = len(grid[0])
    coord = get_exits(grid)
    if len(coord) == 1:
        return (grid, coord[0])
    if not encircled_exit(grid, coord[0]) and not encircled_exit(grid, coord[1]):
        for x in range(lnx):
            for y in range(lny):
                if grid[x][y] == " ":
                    grid[x][y] = 0
        grid[coord[0][0]][coord[0][1]] = 1
        grid[coord[1][0]][coord[1][1]] = 0
        k = 1
        while grid[coord[1][0]][coord[1][1]] == 0:
            grid = make_step(grid, k)
            k += 1
        path = shortest_path(grid, coord[1])
        for x in range(lnx):
            for y in range(lny):
                if grid[x][y] != " " and grid[x][y] != "■":
                    grid[x][y] = " "
        return grid, path
    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(5, 5)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
