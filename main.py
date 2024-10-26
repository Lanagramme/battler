import pygame
from random import randrange

pygame.font.init()

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
      (margin['left'] + x * (size + gutter), margin["top"] + y * (size + gutter)),
      self.dimensions,
    )

  def def_color(self):
    if self.hover: return DARK
    elif self.active: return BLUE
    else: return RED

  def draw(self, SCREEN, pion_color):
    self.color = self.def_color()
    pygame.draw.rect(SCREEN, self.color, self.body)
    if self.pion != None:
      pygame.draw.circle(
        SCREEN, pion_color,
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

    self.cells = [
      [Cell(x, y, margin, gutter, size, False, False, None) 
      for y in range(height)] 
      for x in range(width)
    ]
    self.hover = False
    self.active = False

  def activate(self, x, y, battle):
    # remove active if clicked outside board
    if x == None:
      if self.active: self.active.active = False
      self.active = False
    else:
      target = self.cells[x][y]
      if self.active is not False:
        self.active.active = False
        self.active= False
      # only select pion if turn
      if (target.pion != None 
          and battle.LIST_PIONS[target.pion].team == battle.turn):
        self.active = target
        self.active.active = True
        battle.moving = True
      else:
        return
      pion = target.pion
  def move(self, x,y):
    if self.active is False:
      return True
    else:
      destination = self.cells[x][y]
      if x == self.active.x and y == self.active.y:
        return False
      # Only move to empty case
      if destination.pion != None:
        # change active pion if destination is same team
        if battle.LIST_PIONS[ destination.pion ].team == battle.turn: return True
        return False
      destination.pion = self.active.pion
      self.active.active = False
      self.active.pion = None
      self.active = False
      return False

  def paint(self, SCREEN):
    for x in range(self.X):
      for y in range(self.Y):
        cell = self.cells[x][y]
        cell.hover = True if (x, y) == self.hover else False
        pion_color = (
          battle.TEAMS[battle.LIST_PIONS[cell.pion].team]["color"]
          if cell.pion != None
          else None
        )
        cell.draw(SCREEN, pion_color)

  def get_hovered_cell(self, mouse_x, mouse_y):
    return (
      int((mouse_x - self.margin['left']) / (self.size + self.gutter)),
      int((mouse_y - self.margin["top"]) / (self.size + self.gutter))
    )

class Battle:
  def __init__(self ):
    self.turn = 'Team 1'
    self.LIST_PIONS = []
    self.TEAMS = {
      "Team 1": {"color": PURPLE, "pions": []},
      "Team 2": {"color": CARMIN, "pions": []},
    }
    self.moving = False

  def next_turn(self):
    self.turn = "Team 2" if self.turn == "Team 1" else "Team 1"
    if grid.active is not False:
      grid.active.active = False
    grid.active = False
    title.set_text(self.turn)
    title.set_color(self.TEAMS[self.turn]["color"])

  
  def create(self, team, GX, GY):
    while True:
      X = randrange(GX)
      Y = randrange(GY)
      nouveau_pion = Pion(team, (X, Y))
      if grid.cells[X][Y].pion == None:
        break

    grid.cells[X][Y].pion = len(self.LIST_PIONS)
    self.LIST_PIONS.append(nouveau_pion)

  def start(self, GX, GY, title):
    self.create('Team 1', GX, GY)
    self.create('Team 1', GX, GY)
    self.create('Team 1', GX, GY)
    self.create('Team 2', GX, GY)
    self.create('Team 2', GX, GY)
    self.create('Team 2', GX, GY)
    title.set_text(self.turn)
    title.set_color(self.TEAMS[self.turn]["color"])

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
      for button in buttons:
        button.handle_event(event)

    mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
    clic, _, _ = pygame.mouse.get_pressed(num_buttons=3)

    if not clic:
      self.clicking = False

    if board.collidepoint(mouse_pos):
      grid.hover = grid.get_hovered_cell(mouse_x, mouse_y)
      if clic and not self.clicking:
        self.clicking = True
        if grid.move(grid.hover[0], grid.hover[1]):
          grid.activate(grid.hover[0], grid.hover[1], battle)
    else:
      grid.hover = (None, None)
      if clic and not self.clicking:
        self.clicking = True
        grid.activate(None, None, battle)


  def render(self):
    SCREEN.fill(WHITE)
    self.grid.paint(SCREEN)
    for asset in ui:
      asset.draw(SCREEN)

class Banner:
  def __init__(self, x, color):
    self.x = x
    self.color = color
    self.font = pygame.font.Font(None, 30)  # Font size 30
    self.message = ''  # Placeholder for the message
  
  # Method to set the message text
  def set_text(self, text): 
    self.message = text

  # Method to update the banner color
  def set_color(self, color): 
    self.color = color

  # Method to draw the banner on the screen
  def draw(self, SCREEN):
    # Render the text with the given color
    text_surface = self.font.render(self.message, True, self.color)
    
    # Get the text's rectangle and position it
    rect = text_surface.get_rect()
    rect.centerx = SCREEN.get_rect().centerx  # Center horizontally
    rect.top = self.x  # Set vertical position to self.x

    # Blit the text to the screen
    SCREEN.blit(text_surface, rect)

# FUNCTIONS

# CONSTANTS
WHITE = (255, 241, 215)
BLUE = (93, 100, 190)
GREEN = (0, 255, 0)

RED = (250, 170, 117)
DARK = (245, 121, 85)

PURPLE = (125, 82, 222)
CARMIN = (120, 227, 253)

DARK_BLUE = (0, 100, 200)
BLACK = (0, 0, 0)

MARGIN = {"top": 100, "left":50, "bottom": 100}
GUTTER = 1
CELL_SIZE = 50
COLLS = 9
ROWS = 6

grid = Grid(COLLS, ROWS, MARGIN, GUTTER, CELL_SIZE)
board = pygame.Rect(grid.margin['left'], grid.margin["top"], grid.spanX, grid.spanY)
title = Banner(15,BLACK)
battle = Battle()
battle.start(grid.X, grid.Y, title)


pygame.init()
pygame.time.Clock().tick(60)

HEIGHT = grid.margin["top"] + grid.margin["bottom"] + grid.spanY
WIDTH = grid.margin['left'] * 2 + grid.spanX
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)

# Game state
class Button:
  def __init__(self, x, y, width, height, text, color, hover_color, text_color, font_size, action=None):
    self.rect = pygame.Rect(x, y, width, height)
    self.color = color
    self.hover_color = hover_color
    self.text_color = text_color
    self.font = pygame.font.Font(None, font_size)
    self.text = self.font.render(text, True, self.text_color)
    self.text_rect = self.text.get_rect(center=self.rect.center)
    self.action = action  # Function to be called on click
    self.is_hovered = False

  def draw(self, SCREEN):
    if self.is_hovered:
      pygame.draw.rect(SCREEN, self.hover_color, self.rect)
    else:
      pygame.draw.rect(SCREEN, self.color, self.rect)

    SCREEN.blit(self.text, self.text_rect)

  def handle_event(self, event):
    mouse_pos = pygame.mouse.get_pos()

    self.is_hovered = self.rect.collidepoint(mouse_pos)

    if self.is_hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if self.action:
        self.action()

def on_button_click():
  battle.next_turn()
  print(f"Turn changed to {battle.turn}")

def nothing():
  return


# Button settings
button = Button(15, 15, 100, 50, "Turn", BLUE, DARK_BLUE, BLACK, 36, action=on_button_click)
move = Button(15, HEIGHT-70 , 100, 50, "Move", BLUE, DARK_BLUE, BLACK, 36, action=nothing)
attack = Button(30 + 100, HEIGHT-70 , 100, 50, "Attack", BLUE, DARK_BLUE, BLACK, 36, action=nothing)

buttons = [button, move, attack]
ui = [button, move, attack, title]


game = Game(grid)
game.run()
