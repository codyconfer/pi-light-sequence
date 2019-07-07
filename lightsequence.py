import time
from random import randint
from colors import purecolors
import unicornhat as unicorn


class Sequence:
    delay = 0.15
    #max_nodes = 10
    #skip_ratio = 5
    colors = purecolors


class Grid:
    def __init__(self):
        self.width, self.height = unicorn.get_shape()
        self.top = self.height - 1
        self.right = self.width - 1
        self.left = 0
        self.bottom = 0
        self.points = []
    rotation = 90
    brightness = 0.7


class GridController:
    def __init__(self, grid):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(grid.rotation)
        unicorn.brightness(grid.brightness)

    def plot_points(self, grid):
        unicorn.clear()
        for point in grid.points:
            unicorn.set_pixel(point.x, point.y,
                              point.colour[0], point.colour[1], point.colour[2])
        unicorn.show()

    def update_positions(self, grid):

        for point in grid.points:
            if point.direction == 0:
                point.y += 1
            elif point.direction == 1:
                point.x += 1
            elif point.direction == 2:
                point.y -= 1
            else:
                point.x -= 1
            self.validate_point(point, grid)

    def validate_point(self, point, grid):

        if grid.left < point.x > grid.right:
            grid.points.remove(point)
        if grid.bottom < point.y > grid.top:
            grid.points.remove(point)


class Node:
    def __init__(self, grid):
        direction = randint(0, 3)
        self.direction = direction
        self.direction_coordinate_determination(direction, grid)
        self.set_color()

    def direction_coordinate_determination(self, index, grid):
        switch = {
            0: self.set_direction(self.get_dynamic_position(grid.right), grid.bottom),
            1: self.set_direction(grid.left, self.get_dynamic_position(grid.top)),
            2: self.set_direction(self.get_dynamic_position(grid.right), grid.top),
            3: self.set_direction(grid.right, self.get_dynamic_position(grid.top)),
        }
        return switch.get(index, (self.get_dynamic_position(grid.width - 1), grid.bottom))

    def get_dynamic_position(self, max):
        return randint(0, max)

    def set_direction(self, x, y):
        self.x = x
        self.y = y

    def set_color(self):
        max = len(Sequence.colors) - 1
        self.colour = Sequence.colors[randint(0, max)]


print("""--BEGIN
    unicorn pi light sequence...ctrl + c to exit...
""")

grid = Grid()
controller = GridController(grid)

while True:
    grid.points.append(Node(grid))
    controller.plot_points(grid)
    controller.update_positions(grid)
    time.sleep(Sequence.delay)
