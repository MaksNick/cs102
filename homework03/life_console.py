import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        for x in range(0, self.life.cell_height + 1):
            for y in range(0, self.life.cell_width + 1):
                if x == 0 or x == self.life.cell_height:
                    if y == 0 or y == self.life.cell_width:
                        screen.addstr(x, y, "+")
                    else:
                        screen.addstr(x, y, "-")
                else:
                    screen.addstr(x, y, "|")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        screen.clear()
        for y in range(1, self.life.cell_width + 1):
            for x in range(1, self.life.cell_height + 1):
                if self.life.curr_generation[y - 1][x - 1] == 0:
                    screen.addstr(y, x, " ")
                else:
                    screen.addstr(y, x, "*")

    def run(self) -> None:
        screen = curses.initscr()
        while True:
            self.draw_grid(screen)
            self.draw_borders(screen)
            self.life.step()
            screen.refresh()
        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((24, 80), max_generations=50)
    ui = Console(life)
    ui.run()
