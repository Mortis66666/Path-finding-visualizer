import enum
import queue
import pygame as pg

pg.init()

WIDTH = 400
HEIGHT = 400
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Path finding simulator")

class cell_type(enum.Enum):
    BLANK = 1
    OBSTACLE = 2
    CHECKED = 3
    PATH = 4
    START = 5
    END = 6

class Cell:
    def __init__(self, x: int, y: int, type: cell_type):
        self.x = x
        self.y = y
        self.type = type

    @property
    def color(self):
        match self.type:
            case cell_type.BLANK:
                return 255, 255, 255
            case cell_type.OBSTACLE:
                return 0, 0, 0
            case cell_type.CHECKED:
                return 255, 0, 0
            case cell_type.PATH:
                return 0, 255, 0
            case cell_type.START:
                return 0, 0, 255
            case cell_type.END:
                return 255, 255, 0

    def draw(self):
        pg.draw.rect(
            win,
            self.color,
            (
                self.x * 10,
                self.y * 10,
                10,
                10
            )
        )

grid = [[Cell(x, y, cell_type.BLANK) for x in range(40)] for y in range(40)]

def draw_line():
    for x in range(40):
        pg.draw.line(
            win,
            (0, 0, 0),
            (x*10, 0),
            (x*10, WIDTH-1)
        )
        pg.draw.line(
            win,
            (0, 0, 0),
            (0, x*10),
            (HEIGHT-1, x*10)
        )

def draw():
    win.fill((255, 255, 255))

    for row in grid:
        for cell in row:
            cell.draw()

    draw_line()
    pg.display.update()


def find_neighbors(x, y):
    if x:
        yield x-1, y
    if x < WIDTH//10 - 1:
        yield x+1, y
    if y:
        yield x, y-1
    if y < HEIGHT//10 - 1:
        yield x, y+1

def find_path():
    start = (-1, -1)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.type == cell_type.START:
                start = x, y
                break
    if sum(start) < 0:
        return []

    q = queue.Queue()
    q.put([start])

    while not q.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        path = q.get()
        x, y = path[-1]

        if grid[y][x].type == cell_type.END:
            return path

        for nx, ny in find_neighbors(x, y):
            if grid[ny][nx].type in [cell_type.BLANK, cell_type.END]:
                if grid[ny][nx].type != cell_type.END:
                    grid[ny][nx].type = cell_type.CHECKED
                new_path = path + [(nx,ny)]
                q.put(new_path)
        draw()


def main():
    FPS = 60
    run = True
    clock = pg.time.Clock()

    find = False

    start = False
    end = False
    path = []

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                return
            if event.type == pg.MOUSEBUTTONDOWN and not find:
                x, y = pg.mouse.get_pos()
                x //= 10
                y //= 10
                if not start:
                    grid[y][x].type = cell_type.START
                    start = True
                elif not end:
                    grid[y][x].type = cell_type.END
                    end = True
                else:
                    grid[y][x].type = cell_type.OBSTACLE
            if event.type == pg.KEYDOWN and start and end and pg.key.get_pressed()[pg.K_SPACE]:
                path = find_path()
                
        draw()
        if path:
            x, y = path.pop(0)
            grid[y][x].type = cell_type.PATH

if __name__ == "__main__":
    main()
    pg.quit()

