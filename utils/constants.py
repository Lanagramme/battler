import pygame
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 50
COLLS = 13
ROWS = 9
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)
GUTTER = 1
MARGIN = {"top": (HEIGHT - (ROWS * (CELL_SIZE + GUTTER)) )// 2 , "left":(WIDTH - (COLLS * (CELL_SIZE + GUTTER))) // 2, "bottom": 100}
