import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 250, height: int = 250, cell_size: int = 50, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = True) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []
        if randomize is False:
            for _ in range(self.cell_height):
                col = []
                for _ in range(self.cell_width):
                    col.append(0)
                grid.append(col)
            return grid
        for _ in range(self.cell_height):
            col = []
            for _ in range(self.cell_width):
                col.append(random.choice((0, 1)))
            grid.append(col)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x in range(0, self.height, self.cell_size):
            for y in range(0, self.width, self.cell_size):
                if self.grid[x // self.cell_size][y // self.cell_size] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (y, x, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (y, x, self.cell_size, self.cell_size),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        x = cell[0]
        y = cell[1]
        lnx = len(self.grid) - 1
        lny = len(self.grid[0]) - 1
        cells = []
        if x != 0:
            cells.append(self.grid[x - 1][y])
            if y != 0:
                cells.append(self.grid[x - 1][y - 1])
            if y != lny:
                cells.append(self.grid[x - 1][y + 1])
        if x != lnx:
            cells.append(self.grid[x + 1][y])
            if y != 0:
                cells.append(self.grid[x + 1][y - 1])
            if y != lny:
                cells.append(self.grid[x + 1][y + 1])
        if y != 0:
            cells.append(self.grid[x][y - 1])
        if y != lny:
            cells.append(self.grid[x][y + 1])

        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid = []
        for x in range(0, self.cell_height):
            col = []
            for y in range(0, self.cell_width):
                if (
                    sum(self.get_neighbours((x, y))) == 3
                    and self.grid[x][y] == 0
                    or self.grid[x][y] == 1
                    and (
                        sum(self.get_neighbours((x, y))) == 3
                        or sum(self.get_neighbours((x, y))) == 2
                    )
                ):
                    col.append(1)
                else:
                    col.append(0)
            grid.append(col)
        return grid


if __name__ == "__main__":
    GameOfLife().run()
