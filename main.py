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

  def move(self, destination):
    self.character.moves = self.character.moves - (abs(self.position[0] - destination.x) + abs(self.position[1] - destination.y) )
    origin = grid.cells[self.position[0]][self.position[1]]
    grid.move(origin, destination)

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
  def coords(self):
    return ( self.x,self.y )

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
      ui.set_character( pion.character )
      clean_aoe()

  def move(self, origin,destination):
    pion = origin.pion
    destination.pion = pion
    battle.LIST_PIONS[pion].position = destination.coords()
    destination.active = True
    origin.active = False
    origin.pion = None
    self.active = destination
    clean_aoe()
    ui.set_character( battle.LIST_PIONS[pion].character )
    battle.moving = False

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
    self.attacking = False

  def next_turn(self):
    clean_active()
    clean_aoe()
    self.turn = "Team 2" if self.turn == "Team 1" else "Team 1"
    ui.title.set_text(self.turn)
    ui.title.set_color(self.TEAMS[self.turn]["color"])
    for pion in self.TEAMS[self.turn][ "pions" ]:
      pion.character.moves = pion.character.max_moves

  
  def create(self, team, type, coord, character):
    if type == "random":
      while True:
        X = randrange(coord[0])
        Y = randrange(coord[1])
        nouveau_pion = Pion(team, (X, Y), character)
        if grid.cells[X][Y].pion == None:
          break
    else:
      nouveau_pion =  Pion(team, coord, character)
      X, Y = coord

    grid.cells[X][Y].pion = len(self.LIST_PIONS)
    self.LIST_PIONS.append(nouveau_pion)
    self.TEAMS[team]["pions"].append(nouveau_pion)

  def start(self, GX, GY):
    ui.title.set_text(self.turn)
    ui.title.set_color(self.TEAMS[self.turn]["color"])

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
      if battle.attacking:
        for button in ui.attack_buttons:
          button.handle_event(event)
      elif battle.moving:
          ui.cancel_btn.handle_event(event)
      else:
        for button in ui.character_buttons:
          button.handle_event(event)
      ui.turn_button.handle_event(event)

    mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
    clic, _, _ = pygame.mouse.get_pressed(num_buttons=3)

    if not clic:
      self.clicking = False

    if board.collidepoint(mouse_pos):
      grid.hover = grid.get_hovered_cell(mouse_x, mouse_y)
      if clic and not self.clicking:
        self.clicking = True
        
        x, y = grid.hover
        hover_cell = grid.cells[x][y]
        hover_pion = battle.LIST_PIONS[hover_cell.pion] if hover_cell.pion != None else None
        
        if hover_cell.area == "attack":
          # attaquer ici
          battle.attacking = False
          return
        if hover_pion is not None and hover_pion.team == battle.turn:
          grid.activate(x, y, battle)
          battle.moving = False

        elif hover_pion is None:
          if hover_cell.area == "move":
            battle.LIST_PIONS[grid.active.pion].move(grid.cells[x][y])
          else : 
            clean_aoe()
            clean_active()
    else:
      grid.hover = (None, None)
      if clic and not self.clicking:
        self.clicking = True

  def render(self):
    SCREEN.fill(WHITE)
    self.grid.paint(SCREEN)
    ui.draw()

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
pygame.display.set_caption("Battler")
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
  def __init__(self, name, hp, steps, moves, sprite_sheet, spells, directions, width, height):
    self.name = name
    self.spells = spells
    self.hp = hp
    self.max_hp = hp
    self.moves = moves
    self.max_moves = moves
    self.sprite = sprite_asset(steps, 4, sprite_sheet, directions, width, height)
    self.width = width
    self.height = height
    self.animation = AnimatedSprite(self)
    self.steps = steps

class Ui:
  def __init__(self, title):
    self.font = pygame.font.Font(None, 30)
    self.title = title
    
    self.character = False
    self.turn_button = Button(WIDTH - 15 - 100, 15, 100, 50, "Turn", BLUE, DARK_BLUE, BLACK, 36, action=next_turn)
    self.character_buttons = []
    self.attack_buttons = []

    self.cancel_btn = Button(155, HEIGHT-70, 100, 50, "Cancel", BLUE, DARK_BLUE, BLACK, 36, action=self.cancel_menu)

  def cancel_menu(x):
    clean_aoe()
    battle.moving = False
    battle.attacking = False
    
  def set_character(self,character):
    self.character_buttons.clear()
    self.attack_buttons.clear()
    elements = []

    height = grid.spanY + 105
    margin = grid.margin['left']
    
    name = self.font.render(character.name, True, BLACK)
    elements.append(( name, ( margin,height+10 ) ))

    chp = str(character.hp)
    mhp = str(character.max_hp)
    hp =  self.font.render("Hp: " + chp + "/" + mhp, True, BLACK)
    elements.append(( hp, (margin, height+30) ))

    mv = str(character.moves)
    mmv = str(character.max_moves)
    move_info =  self.font.render("Mp: " + mv + "/" + mmv, True, BLACK)
    elements.append(( move_info, (margin,height+ 55) ))
    
    move = Button(155, HEIGHT-70 , 100, 50, "Move", BLUE, DARK_BLUE, BLACK, 36, action=aoe_move)
    self.character_buttons.append(move)

    attack = Button(170 + 100, HEIGHT-70 , 100, 50, "Attack", BLUE, DARK_BLUE, BLACK, 36, action=aoe_attack)
    self.character_buttons.append(attack)

    i = 0
    for spell in character.spells:
      btn = Button(155  + ( i+1 ) * (100 + 15), HEIGHT-70, 100, 50, spell.name, BLUE, DARK_BLUE, BLACK, 36, action=lambda spell=spell: aoe(grid.active, 'attack', spell.aoe) )
      self.attack_buttons.append(btn)
      i = i+1

    def cancel_menu_atk():
      clean_aoe()
      battle.attacking = False

    self.attack_buttons.append(self.cancel_btn)

    self.character = elements

    
  def draw(self):
    self.title.draw(SCREEN)
    self.turn_button.draw(SCREEN)
    if self.character is not False:
      for element in self.character:
        SCREEN.blit(element[0],element[1])
      if battle.attacking == True:
        for button in self.attack_buttons:
          button.draw(SCREEN)
      elif battle.moving == True:
        self.cancel_btn.draw(SCREEN)
      else:
        for button in self.character_buttons:
          button.draw(SCREEN)

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

class Spell:
  def __init__(self, name, aoe):
    self.name = name
    self.aoe = aoe

def next_turn():
  battle.next_turn()

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
  battle.attacking = True
  # if grid.active is not False:
  #   aoe(grid.active, "attack", 3)

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
    battle.attacking = False
    
    grid.active.active = False
    grid.active = False

    ui.character = False
    ui.buttons = []


ui = Ui(title)

spells = [Spell('Sort 1', 2), Spell("Sort 2", 3), Spell("sort 3", 4) ]

# Characters
Lance = Character('Lance', 12, 4, 5, './sprite_sheet/silver.png', spells, ["bottom", "left", "right", "top"], 60, 60)
Touko = Character('Touko', 12, 4, 4, './sprite_sheet/past.png', spells, ["bottom", "left", "right", "top"], 60, 60)
Azure = Character('Azure', 12, 4, 3, './sprite_sheet/azure.jpg', spells, ["bottom", "left", "right", "top"], 60, 60)
Girl  = Character('Girl', 12, 4, 3, './sprite_sheet/girl.png', spells, ["bottom", "left", "right", "top"], 60, 60)
Demo  = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40)
Demo1 = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40)
Demo2 = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40)

battle = Battle()
battle.create('Team 2', "fix", (11, 2), Demo)
battle.create('Team 2', "fix", (11, 4), Demo2)
battle.create('Team 2', "fix", (11, 6), Demo1)
# battle.create('Team 1', "random", ( 3,grid.Y ) , Girl)
# battle.create('Team 1', "random", ( 3,grid.Y ) , Lance)
# battle.create('Team 1', "random", ( 3,grid.Y ) , Touko)
battle.create('Team 1', "fix", ( 2,2) , Girl)
battle.create('Team 1', "fix", ( 2,4 ) , Lance)
battle.create('Team 1', "fix", ( 2,6 ) , Touko)
battle.start(grid.X, grid.Y)

game = Game(grid)
game.run()
