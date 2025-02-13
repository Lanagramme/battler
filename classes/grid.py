import pygame
from utils.constants import SIZE, SCREEN, HEIGHT, WIDTH, GUTTER, ROWS, COLLS, SIZE, CELL_SIZE, MARGIN
from utils.colors import colors

class Pion:
  def __init__(self, team, position, character):
    self.team = team
    self.position = position
    self.character = character

  def move(self, destination, grid):
    self.character.mp = (self.character.mp - 
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
    print(f"PM: {self.character.max_mp}/{self.character.mp}")
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
    self.is_obstacle = False

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

    self.aoe = set()
    self.prevision_aoe = set()
    self.aoe_templates = {
        "circle": {},
        "line": {},
        "cross": {},
        "cone": {}
    }
    self.precompute_aoe_templates()
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
    """Returns a cell at the specified grid coordinates, or None if out of bounds."""
    if 0 <= x < self.X and 0 <= y  < self.Y:
      return self.cells[x][y]
    return None

  def get_pion(self,x,y):
    return self.cells[x][y].pion 
    
  def activate(self, x, y, ui, ):
    self.battle.attacking = False
    self.deactivate(ui)
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
      distance = character.mp
      character.animation.update()
      self.draw_aoe(self.active, "move", distance, "circle", True)

  def clean_aoe(self):
    if self.aoe != False:
      for cell in self.aoe:
        cell.area = False
      self.aoe.clear()
      self.battle.moving = False

  def clean_prev(self):
    if self.prevision_aoe != False:
      for cell in self.prevision_aoe:
        cell.prev = False
      self.prevision_aoe.clear()
   
  def deactivate(self, ui):
    self.clean_aoe()
    self.battle.attacking = False
    ui.character = False
    ui.buttons = []
    
    if self.active != False:
      if self.active.pion:
        self.active.pion.character.animation.set_idle()
      
      self.active.active = False
      self.active = False

  def remove_pion(self, pion):
    pion.character = False
    self.get_cell(*pion.position).pion = None
    self.battle.LIST_PIONS.remove(pion)

  def set_targets(self, hover):
    x, y = hover
    hover_cell = self.cells[x][y]
    targets = []
    
    if len(self.prevision_aoe):
      for cell in self.prevision_aoe:
        targets.append(cell)
    else:
      targets.append(hover_cell)
      
    return targets



  def precompute_aoe_templates(self):
      """Precompute AoE templates for common shapes and ranges."""
      max_radius = max(self.X, self.Y)
      for radius in range(1, max_radius + 1):
          self.aoe_templates["circle"][radius] = self.generate_circle_template(radius)
          self.aoe_templates["line"][radius] = self.generate_line_template(radius)
          self.aoe_templates["cross"][radius] = self.generate_cross_template(radius)
          self.aoe_templates["cone"][radius] = self.generate_cone_template(radius)

  def draw_aoe_from_caster(self,spell):
    self.battle.active_spell = spell.name
    self.draw_aoe(self.active, "attack", spell.range, spell.aoe, blocking=spell.blocking)
    ###
    return
    
  def draw_aoe(self, origin, area_type, radius, aoe_type, blocking=False):
    """Marks cells in the grid based on AoE type, range, and obstacle interaction."""
    if area_type != 'prev':
        self.clean_aoe()
    else:
        self.clean_prev()

    area = set()
    visited = set()

    # Use precomputed offsets for non-blocking AoEs
    if not blocking and radius in self.aoe_templates[aoe_type]:
        offsets = self.aoe_templates[aoe_type][radius]
        for dx, dy in offsets:
            neighbor = self.get_cell(origin.x + dx, origin.y + dy)
            if neighbor:
                area.add(neighbor)
    else:
        # Use propagation for blocking AoEs
        queue = [(origin, 0)]

        while queue:
            current_cell, distance = queue.pop(0)

            if distance >= radius:
                continue

            # Fetch valid offsets for the AoE type
            if aoe_type == "circle":
              offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cardinal directions
            elif aoe_type == "line":
              offsets = [(-distance, 0), (distance, 0), (0, -distance), (0, distance)]
            else:
              offsets = self.aoe_templates.get(aoe_type, {}).get(radius, [])

            for dx, dy in offsets:
              neighbor = self.get_cell(current_cell.x + dx, current_cell.y + dy)
              if neighbor and neighbor not in visited:
                visited.add(neighbor)

                if blocking and (neighbor.pion or neighbor.is_obstacle):
                  # area.add(neighbor)
                  continue

                area.add(neighbor)
                queue.append((neighbor, distance + 1))

    # Mark the grid cells
    if area_type == 'prev':
      self.prevision_aoe = area
      for cell in self.prevision_aoe:
        cell.prev = True
    elif area_type in ['attack', 'move']:
      self.aoe = area
      for cell in self.aoe:
        cell.area = area_type

  def generate_circle_template(self, radius):
    """Generate a set of offsets for a circular AoE of a given radius."""
    offsets = set()
    for x in range(-radius, radius + 1):
      for y in range(-radius, radius + 1):
        if abs(x) + abs(y) <= radius:
          offsets.add((x, y))
    return offsets

  def generate_line_template(self, radius):
      """Generate a set of offsets for a line AoE of a given radius."""
      offsets = set()
      for step in range(1, radius + 1):
          offsets.update({(-step, 0), (step, 0), (0, -step), (0, step)})
      return offsets

  def generate_cross_template(self, radius):
      """Generate a set of offsets for a cross-shaped AoE of a given radius."""
      offsets = set()
      for step in range(radius + 1):
          offsets.update({(-step, 0), (step, 0), (0, -step), (0, step)})
      return offsets

  def generate_cone_template(self, radius):
      """Generate a set of offsets for a cone-shaped AoE of a given radius."""
      offsets = set()
      for step in range(1, radius + 1):
          base_start = -step + 1
          base_end = step
          for offset in range(base_start, base_end):
              offsets.update({(-step, offset), (step, offset), (offset, -step), (offset, step)})
      return offsets

        

# grid = Grid(COLLS, ROWS, MARGIN, GUTTER, CELL_SIZE)


# HEIGHT = grid.margin["top"] + grid.margin["bottom"] + grid.spanY
# WIDTH = grid.margin['left'] * 2 + grid.spanX
