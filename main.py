import pygame
from random import randrange

pygame.font.init()

# CONSTANTS
WHITE = (255, 241, 215)
BLUE = (93, 100, 190)
GREEN = (44, 199, 33)

ACTIVE = (220, 164, 183)

ORANGE = (250, 170, 117)
RED = (255, 41, 38)
DARK = (245, 121, 85)

PURPLE = (125, 82, 222)
CARMIN = (120, 227, 253)

DARK_BLUE = (0, 100, 200)
BLACK = (0, 0, 0)

MARGIN = {"top": 100, "left":50, "bottom": 100}
GUTTER = 1
CELL_SIZE = 50
COLLS = 13
ROWS = 9

# CLASSES
class Pion:
  def __init__(self, team, position, character):
    self.team = team
    self.position = position
    self.character = character


class Cell:
  def __init__(self, x, y, margin, gutter, size, hover, active, pion):
    self.area = False
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
    if self.hover   : return DARK
    elif self.active: return ACTIVE
    elif self.area == "move"  : return GREEN
    elif self.area == "attack": return RED
    else: return ORANGE

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

    self.aoe = {}

    self.cells = [
      [Cell(x, y, margin, gutter, size, False, False, None) 
      for y in range(height)] 
      for x in range(width)
    ]
    self.hover = False
    self.active = False

  def activate(self, x, y, battle):
    clean_active()
    target = self.cells[x][y]
    if (target.pion != None and battle.LIST_PIONS[target.pion].team == battle.turn):
      pion = battle.LIST_PIONS[target.pion]
      pion.character.animation.idle = False
      self.active = target
      self.active.active = True
      clean_aoe()

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
      if destination.area == "move":
        destination.pion = self.active.pion
        battle.LIST_PIONS[self.active.pion].position = (x, y)
        destination.active = True
        self.active.active = False
        self.active.pion = None
        self.active = destination
        clean_aoe()
        return False
      clean_active()
      clean_aoe()

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

    for pion in battle.LIST_PIONS:
      if pion.character != False:
        if pion.character.animation.idle != True:
          pion.character.animation.update()
        cell = grid.cells[pion.position[0]][pion.position[1]]
        SCREEN.blit(
          pion.character.sprite['bottom'][pion.character.animation.current_frame], 
          (cell.body.centerx - (pion.character.width / 2), cell.body.centery - 20 - (pion.character.width / 2))
        )

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
    clean_active()
    clean_aoe()
    self.turn = "Team 2" if self.turn == "Team 1" else "Team 1"
    title.set_text(self.turn)
    title.set_color(self.TEAMS[self.turn]["color"])

  
  def create(self, team, GX, GY, character):
    while True:
      X = randrange(GX)
      Y = randrange(GY)
      nouveau_pion = Pion(team, (X, Y), character)
      if grid.cells[X][Y].pion == None:
        break

    grid.cells[X][Y].pion = len(self.LIST_PIONS)
    self.LIST_PIONS.append(nouveau_pion)

  def start(self, GX, GY):
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

def get_sprite(sprite_sheet, row, col, width, height):
  sprite = pygame.Surface((width, height), pygame.SRCALPHA)
  sprite.blit(sprite_sheet, (0, 0), (col * width, row * height, width, height))
  sprite.set_colorkey((255,255,255))
  return sprite

def sprite_asset(cols, rows, path, directions, width, height):
  sprite_sheet = pygame.image.load(path)
  sheet_width, sheet_height = sprite_sheet.get_size()
  sprite_width = sheet_width // cols
  sprite_height = sheet_height // cols
  
  sprites = {"top": [], "bottom": [], 'left': [], "right": []}
  sprites['steps'] = cols 
 
  row = 0
  for direction in  directions:
    for col in range(cols):
      sprite = get_sprite(sprite_sheet, row, col, sprite_width, sprite_height)
      sprite = pygame.transform.scale(sprite, (width, height))
      sprites[direction].append(sprite)
    row = row +1
      
  return sprites


# FUNCTIONS
grid = Grid(COLLS, ROWS, MARGIN, GUTTER, CELL_SIZE)
board = pygame.Rect(grid.margin['left'], grid.margin["top"], grid.spanX, grid.spanY)
title = Banner(15,BLACK)


pygame.init()
pygame.time.Clock().tick(60)

HEIGHT = grid.margin["top"] + grid.margin["bottom"] + grid.spanY
WIDTH = grid.margin['left'] * 2 + grid.spanX
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)

class AnimatedSprite:
  def __init__(self, sprite):
    self.parent = sprite
    self.frames = sprite.sprite
    self.animation_speed = 200
    self.current_frame = 0
    self.last_update = pygame.time.get_ticks()
    self.idle = True

  def set_idle(self):
    self.idle = True
    self.current_frame = 0
      
  def update(self):
    if self.idle == True:
      return
    now = pygame.time.get_ticks()

    if now - self.last_update > self.animation_speed:
      self.last_update = now
      self.current_frame = (self.current_frame + 1) % self.parent.steps

# Game state
class Character:
  def __init__(self, name, hp, steps, moves, sprite_sheet, directions, width, height):
    self.name = name
    self.hp = hp
    self.moves = moves
    self.max_moves = moves
    self.sprite = sprite_asset(steps, 4, sprite_sheet, directions, width, height)
    self.width = width
    self.height = height
    self.animation = AnimatedSprite(self)
    self.steps = steps

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

def next_turn():
  battle.next_turn()
  print(f"Turn changed to {battle.turn}")

def nothing():
  return

def neighbors(cell):
  newarea = set([cell])
  newarea.add(cell)
  cells =  grid.cells

  X, Y = cell.x, cell.y

  if Y-1 != -1:
    top    = cells[X][Y-1]
    newarea.add(top)

  if Y+1 != grid.Y:
    bottom = cells[X][Y+1]
    newarea.add(bottom)

  if X-1 != -1:
    left   = cells[X-1][Y]
    newarea.add(left)
    
  if X+1 != grid.X:
    right  = cells[X+1][Y]
    newarea.add(right)

  return newarea

def aoe(origin, type, radius):
  clean_aoe()

  battle.moving = True
  if grid.active is False: return

  cells =  grid.cells
  area = set([origin])
  queue = [(origin, 0)]
  visited = []

  while queue:
    cell, distance = queue.pop(0)

    around = neighbors(cell)
    for neighbor in around:
      if neighbor not in visited:
        visited.append(neighbor)

      if distance  < radius:
        queue.append((neighbor, distance+1))
        area.add(neighbor)

  grid.aoe = area
  for cell in grid.aoe:
    cell.area = type

def aoe_attack():
  if grid.active is not False:
    aoe(grid.active, "attack", 3)

def aoe_move():
  if grid.active is not False:
    character = battle.LIST_PIONS[ grid.active.pion ].character
    distance = character.moves
    character.animation.update()
    aoe(grid.active, "move", distance)

def clean_aoe():
  if grid.aoe != False:
    for cell in grid.aoe:
      cell.area = False
    grid.aoe = False
    

def clean_active():
  if grid.active != False:
    battle.LIST_PIONS[grid.active.pion].character.animation.set_idle()
    grid.active.active = False
    grid.active = False

# Button settings
button = Button(15, 15, 100, 50, "Turn", BLUE, DARK_BLUE, BLACK, 36, action=next_turn)
move = Button(15, HEIGHT-70 , 100, 50, "Move", BLUE, DARK_BLUE, BLACK, 36, action=aoe_move)
attack = Button(30 + 100, HEIGHT-70 , 100, 50, "Attack", BLUE, DARK_BLUE, BLACK, 36, action=aoe_attack)

buttons = [button, move, attack]
ui = [button, move, attack, title]

# Characters
Lance = Character('Lance', 12, 4, 5, './sprite_sheet/silver.png', ["bottom", "left", "right", "top"], 60, 60)
Touko = Character('Touko', 12, 4, 4, './sprite_sheet/past.png', ["bottom", "left", "right", "top"], 60, 60)
Azure = Character('Azure', 12, 4, 3, './sprite_sheet/azure.jpg', ["bottom", "left", "right", "top"], 60, 60)
Girl  = Character('Girl', 12, 4, 3, './sprite_sheet/girl.png', ["bottom", "left", "right", "top"], 60, 60)
Demo  = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', ["bottom", "left", "right", "top"], 34, 40)
Demo1  = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', ["bottom", "left", "right", "top"], 34, 40)
Demo2  = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', ["bottom", "left", "right", "top"], 34, 40)

battle = Battle()
battle.create('Team 1', grid.X, grid.Y, Girl)
battle.create('Team 1', grid.X, grid.Y, Lance)
battle.create('Team 1', grid.X, grid.Y, Touko)
battle.create('Team 2', grid.X, grid.Y, Demo)
battle.create('Team 2', grid.X, grid.Y, Demo2)
battle.create('Team 2', grid.X, grid.Y, Demo1)
battle.start(grid.X, grid.Y)

game = Game(grid)
game.run()
