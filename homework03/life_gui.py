from copy import deepcopy

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 50, speed: int = 1) -> None:
        super().__init__(life)

        # параметры игрового поля
        self.width = 500
        self.height = 500
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
        self.pause = False

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        for x in range(0, self.height, self.cell_size):
            for y in range(0, self.width, self.cell_size):
                if (
                    self.life.curr_generation[x // self.cell_size][y // self.cell_size]
                    == 0
                ):
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
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.life.curr_generation = self.life.create_grid()

        running = True
        count = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    self.pause = not self.pause
                    count = True

                # режим паузы

                if self.pause and event.type == pygame.MOUSEBUTTONDOWN:
                    if count == True:
                        count = False
                        self.life.curr_generation = deepcopy(self.life.prev_generation)
                    if (
                        self.life.curr_generation[event.pos[1] // self.cell_size][
                            event.pos[0] // self.cell_size
                        ]
                        == 0
                    ):
                        self.life.curr_generation[event.pos[1] // self.cell_size][
                            event.pos[0] // self.cell_size
                        ] = 1
                        color = "green"
                    else:
                        self.life.curr_generation[event.pos[1] // self.cell_size][
                            event.pos[0] // self.cell_size
                        ] = 0
                        color = "white"
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (
                            event.pos[0] // self.cell_size * self.cell_size,
                            event.pos[1] // self.cell_size * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                    self.draw_lines()
                    pygame.display.flip()

            if not self.pause:

                # Отрисовка списка клеток
                # Выполнение одного шага игры (обновление состояния ячеек)

                self.draw_grid()
                self.draw_lines()
                self.life.step()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((10, 10), max_generations=50)
    GUI(life).run()
