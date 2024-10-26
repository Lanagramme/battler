import pygame
from random import randrange

# CLASSES
class Pion:
  def __init__(self, team, position):
    self.team = team
    self.position = position


class Cell:
  def __init__(self, x, y, margin, gutter, size, hover, active, pion):
    self.x = x
    self.y = y
    self.padding = 5
    self.dimensions = (size, size)

    self.active = active
    self.hover = hover
    self.color = self.def_color()
    self.pion = pion

    self.body = pygame.Rect(
      (margin + x * (size + gutter), margin + y * (size + gutter)),
      self.dimensions,
    )

  def def_color(self):
    if self.hover:
      return DARK
    elif self.active:
      return BLUE
    else:
      return RED

  def draw(self, SCREEN, pion_color):
    self.color = self.def_color()
    pygame.draw.rect(SCREEN, self.color, self.body)
    if self.pion:
      pygame.draw.circle(
        SCREEN,
        pion_color,
        (self.body.centerx, self.body.centery),
        self.body.width / 2 - self.padding,
      )


class Grid:
  def __init__(self, width, height, margin, gutter, size):
    self.margin = margin
    self.gutter = gutter
    self.size = size

    self.X = width
    self.Y = height
    self.spanX = width * (size + gutter)
    self.spanY = height * (size + gutter)

    self.cells = [[Cell(x, y, margin, gutter, size, False, False, False) for y in range(height)] for x in range(width)]
    self.hover = False
    self.active = (None, None)

    self.turn = 'team1'

  def next_turn(self):
    self.turn = "team2" if self.turn == "team1" else "team1"
  
  def activate(self, x, y):
    self.active = (x, y)

  def paint(self, SCREEN):
    for x in range(self.X):
      for y in range(self.Y):
        cell = self.cells[x][y]
        cell.hover = True if (x, y) == self.hover else False
        cell.active = True if (x, y) == self.active else False
        pion_color = (
          TEAMS[LIST_PIONS[cell.pion].team]["color"]
          if cell.pion
          else None
        )
        cell.draw(SCREEN, pion_color)

  def get_hovered_cell(self, mouse_x, mouse_y):
    return (
      int((mouse_x - self.margin) / (self.size + self.gutter)),
      int((mouse_y - self.margin) / (self.size + self.gutter))
    )

class Game:
  def __init__(self, grid):
    self.grid = grid
    self.clicking = False
    self.playing = True

  def run(self):
    while self.playing:
      self.handle_events()
      self.render()
      pygame.display.flip()

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.playing = False

    mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
    clic, _, _ = pygame.mouse.get_pressed(num_buttons=3)

    if not clic:
      self.clicking = False

    if board.collidepoint(mouse_pos):
      grid.hover = grid.get_hovered_cell(mouse_x, mouse_y)
      if clic and not self.clicking:
        self.clicking = True
        grid.activate(grid.hover[0], grid.hover[1])
    else:
      grid.hover = (None, None)
      if clic and not self.clicking:
        self.clicking = True
        grid.activate(None, None)

  def render(self):
    SCREEN.fill(WHITE)
    self.grid.paint(SCREEN)

# FUNCTIONS
def create(team):
  while True:
    X = randrange(grid.X)
    Y = randrange(grid.Y)
    nouveau_pion = Pion(team, (X, Y))
    if grid.cells[X][Y].pion is False:
      break

  grid.cells[X][Y].pion = len(LIST_PIONS)
  LIST_PIONS.append(nouveau_pion)

# CONSTANTS
WHITE = (255, 241, 215)
BLUE = (93, 100, 190)
GREEN = (0, 255, 0)

RED = (250, 170, 117)
DARK = (245, 121, 85)

PURPLE = (125, 82, 222)
CARMIN = (120, 227, 253)

MARGIN = 50
GUTTER = 1
CELL_SIZE = 50
COLLS = 9
ROWS = 6

grid = Grid(COLLS, ROWS, MARGIN, GUTTER, CELL_SIZE)
board = pygame.Rect(grid.margin, grid.margin, grid.spanX, grid.spanY)

pygame.init()
pygame.time.Clock().tick(60)

HEIGHT = grid.margin * 2 + grid.spanY
WIDTH = grid.margin * 2 + grid.spanX
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)

LIST_PIONS = []
TEAMS = {
  "team1": {"color": PURPLE, "pions": []},
  "team2": {"color": CARMIN, "pions": []},
}

create("team1")
create("team1")
create("team1")
create("team2")
create("team2")
create("team2")

# Game state
game = Game(grid)
game.run()
