import pygame
from utils.constants import SIZE, SCREEN, HEIGHT, WIDTH, GUTTER, ROWS, COLLS, SIZE, CELL_SIZE, MARGIN
from utils.colors import colors


class Pion:
  def __init__(self, team, position, character):
    self.team = team
    self.position = position
    self.character = character

  def move(self, destination, grid):
    self.character.moves = (self.character.moves - 
      (abs(self.position[0] - destination.x) + 
      abs(self.position[1] - destination.y) ))
    origin = grid.cells[self.position[0]][self.position[1]]
    grid.move(origin, destination)

  def loose_pv(self, dmg):
    self.character.hp = self.character.hp - dmg
    return self.character.hp
  
  def detail(self):
    print('======')
    print(f"name: {self.character.name}")
    print(f"hp: {self.character.max_hp}/{self.character.hp}")
    print(f"PM: {self.character.max_moves}/{self.character.moves}")
    print(f"team: {self.team}")
    print(f"tokens: {self.character.tokens}")
    print(f"position: {self.position}")

      
class Cell:
  def __init__(self, x, y, margin, gutter, size, hover, active, pion, turn):
    self.turn = turn
    self.area = False
    self.prev = False
    self.x = x
    self.y = y
    self.padding = 5
    self.dimensions = (size, size)

    self.active = active
    self.hover = hover
    self.pion = pion

    self.body = pygame.Rect(
      (margin['left'] + x * (size + gutter), margin["top"] + y * (size + gutter)),
      self.dimensions,
    )
    
  def coords(self):
    return ( self.x,self.y )

  def get_color(self):
    if self.hover   : return colors.OAK
    elif self.prev == True: return colors.OAK
    elif self.active: return colors.ACTIVE
    elif self.area == "move"  : return colors.GREEN
    elif self.area == "attack": return colors.RED
    else: return colors.ORANGE

  def draw(self, SCREEN, pion_color):
    pygame.draw.rect(SCREEN, self.get_color(), self.body)
    if self.pion != None:
      pygame.draw.circle( SCREEN, pion_color, (self.body.centerx, self.body.centery), self.body.width / 2 - self.padding,)
      if self.pion.team == self.turn.turn:
        pygame.draw.rect(SCREEN, colors.RED, self.body, 3)
      
class Grid:
  def __init__(self, width, height, margin, gutter, size, state):
    self.margin = margin
    self.gutter = gutter
    self.size = size

    self.X = width
    self.Y = height
    self.spanX = width * (size + gutter)
    self.spanY = height * (size + gutter)

    self.aoe = {}
    self.prevision_aoe = {}
    self.board = pygame.Rect(self.margin['left'], self.margin["top"], self.spanX, self.spanY)
    # self.board = False

    self.battle = state
    self.cells = [
      [Cell(x, y, margin, gutter, size, False, False, None, self.battle) 
      for y in range(height)] 
      for x in range(width)
    ]
    self.hover = False
    self.active = False
    for pion in self.battle.LIST_PIONS:
      x, y = pion.position
      
      cell = self.get_cell(x, y)
      if cell: 
        cell.pion = pion

  def get_cell(self, x,y):
    if 0 <= x < self.X and 0 <= y  < self.Y:
      return self.cells[x][y]
    return None

  def get_pion(self,x,y):
    return self.cells[x][y].pion 
    
  def activate(self, x, y, ):
    self.clean_active()
    target = self.get_cell(x,y)
    if (target.pion != None and target.pion.team == self.battle.turn):
      pion = target.pion
      pion.character.animation.idle = False
      self.active = target
      self.active.active = True
      # self.battle.ui.set_character( pion.character )
      self.clean_aoe()

  def move(self, origin,destination):
    pion = origin.pion
    destination.pion = pion
    pion.position = destination.coords()
    origin.pion = None
    if origin == self.active:
      self.active = destination
      origin.active = False
      destination.active = True
    self.clean_aoe()
    # ui.set_character( battle.LIST_PIONS[pion].character )
    self.battle.moving = False

  def draw_turn_outline(self, cell):
    pass

  def paint(self, SCREEN):
    for x in range(self.X):
      for y in range(self.Y):
        cell = self.cells[x][y]
        cell.hover = True if (x, y) == self.hover else False
        pion_color = (
          self.battle.TEAMS[cell.pion.team]["color"]
          if cell.pion != None
          else None
        )
        # if cell.pion and cell.pion.team == self.battle.turn:
          # self.draw_turn_outline(cell)
        # gcc
        cell.draw(SCREEN, pion_color)

    for pion in self.battle.LIST_PIONS:
      if pion.character != False:
        if pion.character.animation.idle != True:
          pion.character.animation.update()
        cell = self.cells[pion.position[0]][pion.position[1]]
        SCREEN.blit(
          pion.character.sprite['bottom'][pion.character.animation.current_frame], 
          (cell.body.centerx - (pion.character.width / 2), cell.body.centery - 20 - (pion.character.width / 2))
        )
    #
  def get_hovered_cell(self, mouse_x, mouse_y):
    return (
      int((mouse_x - self.margin['left']) / (self.size + self.gutter)),
      int((mouse_y - self.margin["top"]) / (self.size + self.gutter))
    )

  def aoe_attack(self):
    self.battle.attacking = True

  def aoe_move(self):
    if self.active is not False:
      self.battle.moving = True
      character = self.active.pion.character
      distance = character.moves
      character.animation.update()
      self.draw_aoe(self.active, "move", distance, "circle")

  def clean_aoe(self):
    if self.aoe != False:
      for cell in self.aoe:
        cell.area = False
      self.aoe = {}
      self.battle.moving = False
      self.battle.attacking = False

  def clean_prev(self):
    if self.prevision_aoe != False:
      for cell in self.prevision_aoe:
        cell.prev = False
      self.prevision_aoe = {}
   
  def clean_active(self):
    if self.active != False:

      if self.active.pion:
        self.active.pion.character.animation.set_idle()
      self.battle.attacking = False
      
      self.active.active = False
      self.active = False

      # ui.character = False
      # ui.buttons = []

  def draw_aoe_from_caster(self,spell):
    self.battle.active_spell = spell.name
    self.draw_aoe(self.active, "attack", spell.range, spell.aoe)
    return
    
  def draw_aoe(self, origin, area_type, radius, aoe_type):
    if area_type != 'prev':
      self.clean_aoe()
    else:
      self.clean_prev()

    cells = self.cells
    visited = set()
    area = {origin}
    if aoe_type == "circle":
      queue = [(origin, 0)]
      while queue:
          cell, distance = queue.pop(0)
          
          if distance >= radius:
              continue

          for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
              nx, ny = cell.x + dx, cell.y + dy
              if 0 <= nx < self.X and 0 <= ny < self.Y:
                  neighbor = cells[nx][ny]

                  if neighbor not in visited:
                    if area_type == "move" and neighbor.pion != None:
                      pass
                    else:
                      visited.add(neighbor)
                      area.add(neighbor)
                      queue.append((neighbor, distance + 1))  # Add the neighbor to the queue

    elif aoe_type == "line":
      start = origin.x - radius if origin.x - radius >= 0 else 0
      end   = origin.x + radius +1 if origin.x + radius+1 <= self.X else self.X
      for x in range(start, end):
        if x != origin.x:
          area.add(cells[x][origin.y])
        else:
          start = origin.y - radius if origin.y - radius >= 0 else 0
          end   = origin.y + radius +1 if origin.y + radius+1 <= self.Y else self.Y
          for cell in cells[x]:
            if cell.y in range(start,end):
                area.add(cell)

      
    if area_type == 'prev':
      self.prevision_aoe = area
      for cell in self.prevision_aoe:
        cell.prev = True  # Assign the area type to each cell
    elif area_type in ['attack', "move"]:
      self.aoe = area
      for cell in self.aoe:
          cell.area = area_type  # Assign the area type to each cell



        

# grid = Grid(COLLS, ROWS, MARGIN, GUTTER, CELL_SIZE)


# HEIGHT = grid.margin["top"] + grid.margin["bottom"] + grid.spanY
# WIDTH = grid.margin['left'] * 2 + grid.spanX
