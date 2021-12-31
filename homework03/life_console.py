import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        screen.clear()
        for y, row in enumerate(self.curr_generation):
            for x, _ in enumerate(row):
                if self.life.curr_generation[y][x] == 0:
                    screen.addstr(y + 1, x + 1, " ")
                else:
                    screen.addstr(y + 1, x + 1, "*")

    def run(self) -> None:
        screen = curses.initscr()
        running = True
        while True:
            self.draw_grid(screen)
            self.draw_borders(screen)
            self.life.step()
            screen.refresh()
            curses.napms(200)
        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((24, 80), max_generations=50)
    ui = Console(life)
    ui.run()
