import pygame
from queue import PriorityQueue

WIDTH = 650
ROWS = 50
GAP = 13
SCREEN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

RED = (238, 52, 48) #START
ORANGE = (255, 172, 32) #END
BLUE = (35, 145, 244) #CLOSED
GREEN = (121, 227, 76) #OPEN
PURPLE = (103, 78, 167) #PATH
BLACK = (0, 0, 0) #BARRIER
WHITE = (255, 255, 255) #BACKGROUND
GREY = (188, 188, 188) #GRID LINES


class Node:
    def __init__(self, col, row, width):
        self.x = col * width
        self.y = row * width
        self.col = col
        self.row = row
        self.width = width
        self.color = WHITE
        self.neighbors = []
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None

    def set_parent(self, parent_node):
        self.parent = parent_node

    def get_parent(self):
        return self.parent

    def set_f(self, f_score):
        self.f = f_score

    def set_g(self, g_score):
        self.g = g_score

    def set_h(self, h_score):
        self.h = h_score

    def get_f(self):
        return self.f

    def get_g(self):
        return self.g

    def get_h(self):
        return self.h

    def is_open(self):
        return self.color == GREEN

    def is_closed(self):
        return self.color == BLUE

    def is_path(self):
        return self.color == PURPLE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == RED

    def is_end(self):
        return self.color == ORANGE

    def get_pos(self):
        return self.col, self.row

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = ORANGE

    def reset(self):
        self.color = WHITE

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.col > 0 and not grid[self.col - 1][self.row].is_barrier():  #LEFT
            self.neighbors.append(grid[self.col - 1][self.row])
        if self.col < ROWS - 1 and not grid[self.col + 1][self.row].is_barrier():  #RIGHT
            self.neighbors.append(grid[self.col + 1][self.row])
        if self.row > 0 and not grid[self.col][self.row - 1].is_barrier():  #UP
            self.neighbors.append(grid[self.col][self.row - 1])
        if self.row < ROWS - 1 and not grid[self.col][self.row + 1].is_barrier():
            self.neighbors.append(grid[self.col][self.row + 1])

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False


def make_grid():
    grid = []
    for i in range(ROWS):
        col = []
        grid.append(col)
        for j in range(ROWS):
            node = Node(i, j, GAP)
            grid[i].append(node)

    return grid


def draw_grid_lines():
    # HORIZONTAL LINES
    for i in range(ROWS):
        pygame.draw.line(SCREEN, GREY, (0, i * GAP), (WIDTH, i * GAP))
    # VERTICAL LINES
    for i in range(ROWS):
        pygame.draw.line(SCREEN, GREY, (i * GAP, 0), (i * GAP, WIDTH))


def draw_grid(grid):
    for i in range(ROWS):
        for j in range(ROWS):
            grid[i][j].draw()
    draw_grid_lines()
    pygame.display.update()


def get_clicked_grid_pos(pos):
    x, y = pos
    col = x // GAP
    row = y // GAP
    return col, row


def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = abs(x2 - x1) + abs(y2 - y1)
    return distance


def astar(grid, start, end):
    queue = PriorityQueue()
    yet_to_visit = set()
    yet_to_visit.add(start)
    visited = set()

    #Set inital f, g, and h scores for all nodes in grid
    for col in grid:
        for node in col:
            h_score = h(node.get_pos(), end.get_pos())
            node.set_h(h_score)
            node.set_g(float('inf'))
            node.set_f(node.get_g() + node.get_h())
            node.update_neighbors(grid)
    start.set_g(0)
    start.set_f(start.get_g() + start.get_h())

    queue.put((0, start))

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()[1]
        yet_to_visit.remove(current)

        if current == end:
            parent = current.get_parent()
            while parent:
                if parent != start and parent != end:
                    parent.make_path()
                parent = parent.get_parent()
                draw_grid(grid)
                end.make_end()
            return

        for node in current.neighbors:
            if current.get_g() + 1 < node.get_g():
                node.set_g(current.get_g() + 1)
                node.set_f(node.get_g() + node.get_h())
                node.set_parent(current)
                if node not in yet_to_visit:
                    queue.put((node.get_f(), node))
                    yet_to_visit.add(node)
                    node.make_closed()
            draw_grid(grid)

        if current != start:
            current.make_closed()


def main():
    grid = make_grid()
    start = None
    end = None
    run = True

    while run:
        draw_grid(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif pygame.mouse.get_pressed()[0]:  #LEFT CLICK
                clicked_pos = pygame.mouse.get_pos()
                col, row = get_clicked_grid_pos(clicked_pos)
                clicked_node = grid[col][row]
                if not start:
                    start = clicked_node
                    start.make_start()
                elif not end and not clicked_node.is_start():
                    end = clicked_node
                    end.make_end()
                elif not clicked_node.is_start() and not clicked_node.is_end():
                    clicked_node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  #RIGHT CLICK
                clicked_pos = pygame.mouse.get_pos()
                col, row = get_clicked_grid_pos(clicked_pos)
                clicked_node = grid[col][row]
                if clicked_node.is_start():
                    start = None
                    clicked_node.reset()
                elif clicked_node.is_end():
                    end = None
                    clicked_node.reset()
                else:
                    clicked_node.reset()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #START ALGORITHM
                astar(grid, start, end)


main()