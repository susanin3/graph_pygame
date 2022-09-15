import drawing
from colors import Colors
import random as rnd
import pygame as pg

DRAG_BUSY = False
IDS = []
MAX_ID = 0


def generate_vertex_id():
    global MAX_ID
    MAX_ID += 1
    return MAX_ID


class CoveredBusy:
    def __init__(self, busy: bool = False, on: int = None):
        self.busy = busy
        self.on = on

    def __bool__(self):
        return self.busy

    def __str__(self):
        return str(self.busy)

    def __int__(self):
        return int(self.busy)


COVER_BUSY = CoveredBusy()


class Vertex:
    def __init__(self, id_, screen, mouse, con_to, position=(0, 0), radius=10, color=Colors.DarkCyan, width=1, text="", selected=False):
        self.id_ = id_
        self.screen = screen
        self.mouse = mouse
        self.con_to = con_to
        self.position = position
        self.radius = radius
        self.color = color
        self.width = width
        self.text = str(id_)
        self.selected = selected
        self.covered = False
        self.dragging = False
        self.shape = drawing.Shape.Circle(self.screen, color=self.color, position=self.position, radius=self.radius, width=self.width)
        self.selected_shape = drawing.Shape.Circle(self.screen, color=self.color, position=self.position, radius=self.radius + 5, width=0)
        self.text_shape = drawing.Text(self.screen, self.text, (10, 10), Colors.WhiteSmoke)

    def draw(self):
        self.shape.position = self.position
        if self.selected:
            self.selected_shape.position = self.position
            self.selected_shape.color = self.selected_color()
            self.selected_shape.draw()
        if self.covered or self.dragging or self.selected:
            self.shape.width = 0
        else:
            self.shape.width = self.width
        self.shape.draw()
        if self.text != "":
            pass
            # self.text_shape.position = (self.position[0] - self.radius//2, self.position[1] - self.radius//2)
            self.text_shape.position = (self.position[0] - self.radius, self.position[1] - self.radius)
            self.text_shape.draw()

    def selected_color(self):
        res = list(self.color)
        res[0] = abs(res[0] - 100)
        res[1] = abs(res[1] - 100)
        res[2] = abs(res[2] - 100)
        return res

    def is_covered(self):
        global COVER_BUSY
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
        global COVER_BUSY
        self.is_covered()
        if not COVER_BUSY:
            COVER_BUSY.busy = self.covered
            COVER_BUSY.on = self.id_

        self.drag()
        self.draw()


class Edge:
    def __init__(self, screen, position: tuple = ((0, 0), (0, 0)), weight=0, width=1, color=Colors.Orchid):
        self.screen = screen
        self.position = position
        self.weight = weight
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
    def __init__(self, screen, mouse):
        self.screen = screen
        self.mouse = mouse
        self.vertexes = []
        self.stat_text_shape = drawing.Text(self.screen, "", (10, 10), Colors.WhiteSmoke)
        self.stat_text = ""

    def draw(self, events):
        for v in self.vertexes:
            v.iteration(events)

    def is_any_vertex_covered(self):
        return len(self.vertexes) > 0 and any([i.covered for i in self.vertexes])
        # global COVER_BUSY
        # if len(self.vertexes) > 0 and any([i.covered for i in self.vertexes]):
        #     COVER_BUSY.busy = True
        #     COVER_BUSY.on = min([i.id_ for i in self.vertexes if i.covered])
        #     # COVER_BUSY.by = [i.id_ for i in self.vertexes if i.covered][0]
        #     print([i.id_ for i in self.vertexes if i.covered])
        # else:
        #     COVER_BUSY.busy = False
        #     COVER_BUSY.on = None
        # return COVER_BUSY.busy

    def set_vertex_selected(self, id_, selected=None):
        for c, v in enumerate(self.vertexes):
            if v.id_ == id_:
                if selected is None:
                    self.vertexes[c].selected = not self.vertexes[c].selected
                else:
                    self.vertexes[c].selected = selected

    def get_selected(self):
        return [i.id_ for i in self.vertexes]

    def set_adjacency(self, ids):
        for c, v in enumerate(self.vertexes):
            for i in ids:
                if v.id_ in ids and v.id_ != i:
                    self.vertexes[c].con_to.append(i)

    def iteration(self, events):
        global COVER_BUSY, DRAG_BUSY
        # self.is_any_vertex_covered()
        if not self.is_any_vertex_covered():
            COVER_BUSY.busy = False
            COVER_BUSY.on = None
        self.stat_text = f"{COVER_BUSY.busy=}   {COVER_BUSY.on=}    {DRAG_BUSY=}"
        self.stat_text_shape.text = self.stat_text
        self.stat_text_shape.draw()
        for i in events:
            if i.type == pg.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if not COVER_BUSY and not DRAG_BUSY:
                        self.vertexes.append(Vertex(id_=generate_vertex_id(), screen=self.screen, mouse=self.mouse, con_to=[], position=self.mouse.get_pos()))
                if i.button == 3:
                    if COVER_BUSY.on is not None:
                        for v in self.vertexes:
                            if v.id_ == COVER_BUSY.on:
                                self.set_vertex_selected(v.id_)
            if i.type == pg.KEYDOWN:
                if i.key == pg.K_KP_ENTER:
                    selected = self.get_selected()
                    if len(selected) == 2:
                        self.set_adjacency(selected)

        self.draw(events)


"""
{
Vertex(con_to=["v1", "v2", "v3"]), Vertex(), Vertex(), Vertex(), Vertex()
}

[
[]
]

"""
