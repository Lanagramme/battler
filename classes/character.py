import pygame

class Character:
  def __init__(self, name, hp, steps, moves, sprite_sheet, spells, directions, width, height, offsetx = 0, offsety = 0):
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
    self.offsetx = offsetx
    self.offsety = offsety
    self.tokens = { "fire": 0, "water": 0, "earth": 0}

  def add_tokens(self, element, qte):
    self.tokens[element] = self.tokens[element] + qte

  def remove_tokens(self, element, qte):
    self.tokens[element] = self.tokens[element] + qte

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
