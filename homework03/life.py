import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.cell_height, self.cell_width = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = True) -> Grid:
        grid = [[[""] for i in range(self.cell_width)] for j in range(self.cell_height)]
        if randomize == False:
            for x in range(self.cell_height):
                for y in range(self.cell_width):
                    grid[x][y] = 0
            return grid
        else:
            for x in range(self.cell_height):
                for y in range(self.cell_width):
                    grid[x][y] = random.choice((0, 1))
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x = cell[0]
        y = cell[1]
        lnx = len(self.curr_generation) - 1
        lny = len(self.curr_generation[0]) - 1
        cells = []
        if x == 0 and y == 0:
            cells.append(self.curr_generation[0][1])
            cells.append(self.curr_generation[1][0])
            cells.append(self.curr_generation[1][1])
            cells = [i for i in cells if i != 0]
            return cells
        if x == 0 and y == lny:
            cells.append(self.curr_generation[0][lny - 1])
            cells.append(self.curr_generation[1][lny])
            cells.append(self.curr_generation[1][lny - 1])
            cells = [i for i in cells if i != 0]
            return cells
        if x == lnx and y == 0:
            cells.append(self.curr_generation[lnx][1])
            cells.append(self.curr_generation[lnx - 1][0])
            cells.append(self.curr_generation[lnx - 1][1])
            cells = [i for i in cells if i != 0]
            return cells
        if x == lnx and y == lny:
            cells.append(self.curr_generation[lnx - 1][lny])
            cells.append(self.curr_generation[lnx][lny - 1])
            cells.append(self.curr_generation[lnx - 1][lny - 1])
            cells = [i for i in cells if i != 0]
            return cells
        if x == 0:
            for ik in range(0, 2):
                for jk in range(y - 1, y + 2):
                    if x != ik and y != jk:
                        cells.append(self.curr_generation[ik][jk])
            cells = [i for i in cells if i != 0]
            return cells
        if x == lnx:
            for ik in range(lnx - 1, lnx + 1):
                for jk in range(y - 1, y + 2):
                    if x != ik and y != jk:
                        cells.append(self.curr_generation[ik][jk])
            cells = [i for i in cells if i != 0]
            return cells
        if y == 0:
            for ik in range(x - 1, x + 2):
                for jk in range(0, 2):
                    if x != ik and y != jk:
                        cells.append(self.curr_generation[ik][jk])
            cells = [i for i in cells if i != 0]
            return cells
        if y == lny:
            for ik in range(x - 1, x + 2):
                for jk in range(lny - 1, lny + 1):
                    if x != ik and y != jk:
                        cells.append(self.curr_generation[ik][jk])
            cells = [i for i in cells if i != 0]
            return cells
        for ik in range(x - 1, x + 2):
            for jk in range(y - 1, y + 2):
                if x != ik and y != jk:
                    cells.append(self.curr_generation[ik][jk])
        cells = [i for i in cells if i != 0]
        return cells

    def get_next_generation(self) -> Grid:
        grid = [[[""] for i in range(self.cell_width)] for j in range(self.cell_height)]
        for x in range(self.cell_height):
            for y in range(self.cell_width):
                if (
                    len(self.get_neighbours((x, y))) == 2
                    or len(self.get_neighbours((x, y))) == 3
                ):
                    grid[x][y] = 1
                else:
                    grid[x][y] = 0
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if self.is_changing and not self.is_max_generations_exceeded:
            self.prev_generation = deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.generations += 1
            self.save(pathlib.Path("glider-4-steps.txt"))

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = [int(line[i]) for i in range(len(line) - 1)]
                if line:
                    grid.append(line)
        life = GameOfLife((len(grid), len(grid[0])), max_generations=50)
        life.curr_generation = grid
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for _, line in enumerate(self.curr_generation):
                for _, e in enumerate(line):
                    f.write(str(e))
                f.write("\n")


if __name__ == "__main__":
    life = GameOfLife.from_file(pathlib.Path("glider.txt"))
    steps = 4  # задает количество итераций
    for _ in range(steps):
        life.step()
