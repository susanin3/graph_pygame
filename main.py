import sys

import pygame as pg

from colors import Colors
from graph import Graph, Vertex, Edge, DRAG_BUSY

pg.init()
size = width, height = 900, 900
screen = pg.display.set_mode(size)
# surface = pg.Surface()
clock = pg.time.Clock()
font = pg.font.Font(pg.font.get_default_font(), 20)
font.underline = Colors.WhiteSmoke
# v = Vertex(screen, mouse=pg.mouse, position=(100, 100), radius=10, width=1)
# v1 = Vertex(screen, mouse=pg.mouse, position=(100, 100), radius=10, width=1)
# v2 = Vertex(screen, mouse=pg.mouse, position=(100, 100), radius=10, width=1)
# e = Edge(screen)

g = Graph()

while 1:
    screen.fill(Colors.Black)
    clock.tick(60)
    events = pg.event.get()



    # v.iteration(events)
    # v1.iteration(events)
    # v2.iteration(events)
    # e.position = (v1.position, v2.position)
    # e.draw()
    for event in events:
        # print(event)
        if event.type == pg.KEYDOWN:
            if event.key == 27:
                sys.exit()
        if event.type == pg.QUIT:
            sys.exit()

    # text_surface = font.render(f"{dt.datetime.now()}", True, white)
    # screen.blit(text_surface, dest=(0, 0))
    # pg.display.flip()
    pg.display.update()
