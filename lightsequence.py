import time
from random import randint
from colors import purecolors
import unicornhat as unicorn


class Sequence:
    delay = 0.08
    max_nodes = 10
    skip_ratio = 5
    colors = purecolors


class Grid:
    rotation = 0
    brightness = 0.5
    # calculated values
    width, height = unicorn.get_shape()
    left = 0
    right = width - 1
    top = height - 1
    bottom = 0
    points = []


class Sequencer:
    def __init__(self):
        self.welcome()
        controller = GridController()
        while True:
            if len(Grid.points) < Sequence.max_nodes and randint(0, Sequence.skip_ratio) > 1:
                Grid.points.append(Node())
            controller.plot_points()
            controller.update_positions()
            time.sleep(Sequence.delay)

    def welcome(self):
        print("""--BEGIN
            unicorn pi light sequence...ctrl + c to exit...
        """)


class GridController:
    def __init__(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(Grid.rotation)
        unicorn.brightness(Grid.brightness)

    def plot_points(self):
        unicorn.clear()
        for point in Grid.points:
            unicorn.set_pixel(point.x, point.y,
                              point.colour[0], point.colour[1], point.colour[2])
        unicorn.show()

    def update_positions(self):

        for point in Grid.points:
            if point.direction == 1:
                point.y += 1
            elif point.direction == 2:
                point.x += 1
            elif point.direction == 3:
                point.y -= 1
            else:
                point.x -= 1
            self.validate_point(point)

    def validate_point(self, point):

        if Grid.right < point.x < Grid.left:
            Grid.points.remove(point)
        if Grid.top < point.y < Grid.bottom:
            Grid.points.remove(point)


class Node:
    def __init__(self):
        self.direction = randint(0, 3)
        self.direction_coordinate_determination(self.direction)
        self.set_color()

    def direction_coordinate_determination(self, index):
        switch = {
            0: self.set_direction(self.get_dynamic_position(Grid.width - 1), 0),
            1: self.set_direction(0, self.get_dynamic_position(Grid.height - 1)),
            2: self.set_direction(self.get_dynamic_position(Grid.width - 1), Grid.height - 1),
            3: self.set_direction(Grid.width - 1, self.get_dynamic_position(Grid.height - 1)),
        }
        return switch.get(index, (self.get_dynamic_position(Grid.width - 1), 0))

    def get_dynamic_position(self, max):
        return randint(0, max)

    def set_direction(self, x, y):
        self.x = x
        self.y = y

    def set_color(self):
        max = len(Sequence.colors) - 1
        self.colour = Sequence.colors[randint(0, max)]


sequencer = Sequencer()