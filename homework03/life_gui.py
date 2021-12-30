import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI
from copy import deepcopy


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 50, speed: int = 1) -> None:
        super().__init__(life)

        # параметры игрового поля
        self.width = 250
        self.height = 250
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.paused = False

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for x in range(0, self.height, self.cell_size):
            for y in range(0, self.width, self.cell_size):
                if self.life.curr_generation[x // self.cell_size][y // self.cell_size] == 0:
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

    def run(self) -> None:
        None


if __name__ == "__main__":
    life = GameOfLife((5, 5), max_generations=50)
    GUI(life).run()
