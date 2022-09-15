import pygame as pg
import drawing
from colors import Colors


class Widget:
    def __init__(self, position):
        self.position = position


class Button(Widget):
    def __init__(self, screen, mouse, position, text='Button', onclick=None):
        super().__init__(position)
        if text is None:
            raise Exception("Text can't be None")
        self.screen = screen
        self.mouse = mouse
        self.text = text
        self.onclick = onclick
        self.size = (70, 20)
        self.text_shape = drawing.Text(screen=screen, text=self.text, position=self.position, color=Colors.WhiteSmoke)
        self.shape = drawing.Shape.Rect(screen=screen, color=Colors.WhiteSmoke, position=self.position, size=self.size, width=1, border_radius=1)

    def draw(self):
        self.text_shape.draw()
        self.shape.draw()

    def is_covered(self):
        x, y = self.position
        x1, y1 = x + self.size[0], y + self.size[1]
        mx, my = self.mouse.get_pos()
        return x < mx < x1 and y < my < y1

    def iteration(self, events):
        self.draw()
        for i in events:
            if i.type == pg.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if callable(self.onclick) and self.is_covered():
                        self.onclick()
