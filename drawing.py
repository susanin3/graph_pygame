import pygame as pg


class Shape:
    class Circle:
        def __init__(self, screen, color, position, radius, width):
            self.screen = screen
            self.color = color
            self.position = position
            self.radius = radius
            self.width = width

        def draw(self):
            pg.draw.circle(self.screen, self.color, self.position, self.radius, self.width)

    class Rect:
        def __init__(self, screen, color, position, size, width, border_radius):
            self.screen = screen
            self.color = color
            self.position = position
            self.size = size
            self.border_radius = border_radius
            self.width = width

        def draw(self):
            pg.draw.rect(self.screen, color=self.color, width=self.width, border_radius=self.border_radius, rect=(self.position[0], self.position[1], self.size[0], self.size[1]))

    class Line:
        def __init__(self, screen, start_point, end_point, color, width):
            self.screen = screen
            self.start_point = start_point
            self.end_point = end_point
            self.color = color
            self.width = width

        def draw(self):
            pg.draw.line(surface=self.screen, color=self.color, start_pos=self.start_point, end_pos=self.end_point, width=self.width)

    class Lines:
        def __init__(self, screen, points, color, width, closed):
            self.screen = screen
            self.points = points
            self.color = color
            self.width = width
            self.closed = closed

        def draw(self):
            pg.draw.lines(surface=self.screen, color=self.color, points=self.points, width=self.width, closed=self.closed)


class Text:
    def __init__(self, screen, text, position, color, font=None):
        self.text = text
        self.position = position
        self.color = color
        self.screen = screen
        self.font = font if font else pg.font.Font(pg.font.get_default_font(), 15)

    def draw(self):
        text_surface = self.font.render(self.text, True, self.color)
        self.screen.blit(text_surface, dest=self.position)

    def get_size(self) -> tuple:
        return self.font.size(self.text)
