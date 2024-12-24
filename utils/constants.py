import pygame

WIDTH = 900
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)

ROWS = 9
COLLS = 13
GUTTER = 1
CELL_SIZE = 50

MARGIN = {"top": (HEIGHT - (ROWS * (CELL_SIZE + GUTTER)) )// 2 , "left":(WIDTH - (COLLS * (CELL_SIZE + GUTTER))) // 2, "bottom": 100}
