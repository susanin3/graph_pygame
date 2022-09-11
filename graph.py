import drawing
from colors import Colors
import random as rnd

DRAG_BUSY = False
IDS = []


class Vertex:
    def __init__(self, screen, mouse, position=(0, 0), radius=10, color=Colors.DarkCyan, width=1, text="", selected=False):
        self.id_ = None
        self.screen = screen
        self.position = position
        self.radius = radius
        self.color = color
        self.width = width
        self.text = text
        self.selected = selected
        self.mouse = mouse
        self.covered = False
        self.dragging = False
        self.shape = drawing.Shape.Circle(self.screen, color=self.color, position=self.position, radius=self.radius, width=self.width)

    def draw(self):
        self.shape.position = self.position
        if self.covered or self.dragging:
            self.shape.width = 0
        else:
            self.shape.width = self.width
        self.shape.draw()
        if self.text != "":
            pass
            # drawing.Text.draw()

    def is_covered(self):
        x, y = self.position
        x0, y0 = self.mouse.get_pos()
        self.covered = (x - x0) ** 2 + (y - y0) ** 2 <= self.radius ** 2
        return self.covered

    def drag(self):
        global DRAG_BUSY
        pressed = bool(self.mouse.get_pressed()[0])
        if (self.covered and pressed and not DRAG_BUSY) or self.dragging:
            self.position = self.mouse.get_pos()
            DRAG_BUSY = True
            self.dragging = True
        if not pressed:
            self.dragging = False
            DRAG_BUSY = False

    def iteration(self, events):
        self.is_covered()
        self.drag()
        self.draw()


class Edge:
    def __init__(self, screen, position: tuple = ((0, 0), (0, 0)), width=1, color=Colors.Orchid):
        self.screen = screen
        self.position = position
        self.width = width
        self.color = color
        self.shape = drawing.Shape.Line(screen, self.position[0], self.position[1], Colors.Plum, 1)

    def draw(self):
        self.shape.start_point = self.position[0]
        self.shape.end_point = self.position[1]
        self.shape.draw()

    def iteration(self, events):
        self.draw()


class Graph:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pass

    def iteration(self):
        self.draw()
