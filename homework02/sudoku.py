import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[int], n: int) -> tp.List[tp.List[int]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    k = 0
    A = [[0] * n for i in range(n)]

    for i in range(n):
        for j in range(n):
            A[i][j] = values[k]
            k += 1
    return A


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row = []
    for i in range(len(grid)):
        row.append(grid[pos[0]][i])

    return row


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for i in range(len(grid)):
        col.append(grid[i][pos[1]])

    return col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    k = 0
    i1 = pos[0] - pos[0] % 3
    j1 = pos[1] - pos[1] % 3
    for i in range(i1, i1 + 3):
        for j in range(j1, j1 + 3):
            block.append(grid[i][j])
            k += 1
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]] or bool:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    empty = []
    for i in range(9):
        for j in range(9):
            if grid[i][j] == ".":
                empty.append(i)
                empty.append(j)
                break
        if len(empty) != 0:
            break
    if empty == []:
        return tuple([-1, -1])
    else:
        return tuple(empty)


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values: list = []
    sr = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    sr1 = get_row(grid, pos)
    sr2 = get_col(grid, pos)
    sr3 = get_block(grid, pos)
    values1 = []
    for i in range(9):
        p1 = sr[i] in sr1
        p2 = sr[i] in sr2
        p3 = sr[i] in sr3
        if p1 == False and p2 == False and p3 == False:
            values1.append(sr[i])
    return set(values1)


def proverka(grid):
    pr = 1
    for i in range(9):
        if len(set(get_row(grid, (0, i)))) != len(get_row(grid, (0, i))):
            pr = 0
            break
        if len(set(get_col(grid, (i, 0)))) != len(get_col(grid, (0, i))):
            pr = 0
            break
        if len(set(get_block(grid, (1, i)))) != len(get_block(grid, (1, i))):
            pr = 0
            break
        if len(set(get_block(grid, (4, i)))) != len(get_block(grid, (4, i))):
            pr = 0
            break
        if len(set(get_block(grid, (7, i)))) != len(get_block(grid, (7, i))):
            pr = 0
            break
    return pr


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty_pos = find_empty_positions(grid)
    if empty_pos == (-1, -1):
        return grid
    posib_pos_list = list(find_possible_values(grid, empty_pos))
    for i in range(len(posib_pos_list)):
        grid[empty_pos[0]][empty_pos[1]] = posib_pos_list[i]
        if check_grid(grid, empty_pos[0], empty_pos[1]) == True:
            if solve(grid):
                return grid
            grid[empty_pos[0]][empty_pos[1]] = "."
        else:
            grid[empty_pos[0]][empty_pos[1]] = "."
    return False


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    pr = True
    for i in range(9):
        if (
            len(set(get_row(solution, (0, i)))) != len(get_row(solution, (0, i)))
            or get_row(solution, (0, i)).count(".") != 0
        ):
            pr = False
            break
        if (
            len(set(get_col(solution, (i, 0)))) != len(get_col(solution, (i, 0)))
            or get_col(solution, (i, 0)).count(".") != 0
        ):
            pr = False
            break
        if (
            len(set(get_block(solution, (1, i)))) != len(get_block(solution, (1, i)))
            or get_block(solution, (1, i)).count(".") != 0
        ):
            pr = False
            break
        if (
            len(set(get_block(solution, (4, i)))) != len(get_block(solution, (4, i)))
            or get_block(solution, (4, i)).count(".") != 0
        ):
            pr = False
            break
        if (
            len(set(get_block(solution, (7, i)))) != len(get_block(solution, (7, i)))
            or get_block(solution, (7, i)).count(".") != 0
        ):
            pr = False
            break
    return pr


def check_grid(grid, x, y):
    A = get_row(grid, (x, 0))
    B = get_col(grid, (0, y))
    C = get_block(grid, (x, y))
    A1 = []
    B1 = []
    C1 = []
    for i in range(9):
        if A[i] != ".":
            A1.append(A[i])
        if B[i] != ".":
            B1.append(B[i])
        if C[i] != ".":
            C1.append(C[i])
    if (
        len(set(A1)) == len(A1)
        and len(set(B1)) == len(B1)
        and len(set(C1)) == len(C1)
        and len(A1) != 0
        and len(B1) != 0
        and len(C1) != 0
    ):
        return True
    else:
        return False


import random


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = [["." for i in range(9)] for i in range(9)]
    for i in range(N):
        x, y = random.randint(0, 8), random.randint(0, 8)
        while grid[x][y] != ".":
            x, y = random.randint(0, 8), random.randint(0, 8)
        grid[x][y] = random.randint(1, 9)
        while check_grid(grid, x, y) != True:
            grid[x][y] = random.randint(1, 9)

    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
