import pygame
pygame.font.init()
from utils.colors import colors
from utils.constants import HEIGHT, WIDTH

class Ui:
  def __init__(self, current_turn, WIDTH, HEIGHT, battle):
    self.font = pygame.font.Font(None, 30)
    self.battle = battle
    self.set_turn(current_turn)
    self.clear_aoe = False

    
    self.character = False
    self.turn_button = Button(WIDTH - 15 - 100, 15, 100, 50, "Turn", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36, action=self.battle.next_turn)
    self.character_buttons = []
    self.attack_buttons = []

    self.cancel_btn = Button(175, HEIGHT-60, 100, 50, "Cancel", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36, action=lambda: self.cancel_menu(battle))

  def set_turn(self, current_turn):
    self.current_turn = Banner(15, colors.BLACK) 
    self.current_turn.set_text(current_turn)
    self.current_turn.set_color(self.battle.TEAMS[self.battle.turn][ "color" ])

  def cancel_menu(self, battle):
      self.clear_aoe = True
      battle.moving = False
      battle.attacking = False

  def set_character(self, character, battle, grid, ):
      self.character_buttons.clear()
      self.attack_buttons.clear()
      elements = []

      height = grid.spanY + 105
      margin = grid.margin['left']
      
      self.add_character_info(elements, character, margin, height, )
      self.create_character_buttons(battle, grid)
      self.create_spell_buttons(character, battle, grid)
      self.attack_buttons.append(self.cancel_btn)
      self.character = elements

  def add_character_info(self, elements, character, margin, height, ):
      name = self.font.render(character.name, True, colors.BLACK)
      hp = self.font.render(f"Hp: {character.hp}/{character.max_hp}", True, colors.BLACK)
      move_info = self.font.render(f"Mp: {character.moves}/{character.max_moves}", True, colors.BLACK)
    
      elements.append((name, (margin, height - 30)))
      elements.append((hp, (margin, height - 10)))
      elements.append((move_info, (margin, height + 10)))

  def create_character_buttons(self, battle, grid):
      move = Button(175, HEIGHT - 60, 100, 50, "Move", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36, action=grid.aoe_move)
      attack = Button(190 + 100, HEIGHT - 60, 100, 50, "Attack", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36, action=grid.aoe_attack)
    
      self.character_buttons.append(move)
      self.character_buttons.append(attack)

  def create_spell_buttons(self, character, battle, grid):
      for i, spell in enumerate(character.spells):
          btn = Button(175 + (i + 1) * (100 + 15), HEIGHT - 60, 100, 50, spell["name"], colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36,
                       action=lambda spell=spell: grid.draw_aoe_from_caster(spell))
          self.attack_buttons.append(btn)

  # def cast_spell(self, spell, castor, battle, aoe):
  #     aoe(castor, 'attack', spell["range"], spell["aoe"])
  #     battle.active_spell = spell['name']

  def draw(self, SCREEN):
      self.current_turn.draw(SCREEN)
      self.turn_button.draw(SCREEN)
      if self.character:
          for element in self.character:
              SCREEN.blit(element[0], element[1])
          self.draw_buttons(SCREEN)

  def draw_buttons(self, SCREEN):
      if self.battle.attacking:
          for button in self.attack_buttons:
              button.draw(SCREEN)
      elif self.battle.moving:
          self.cancel_btn.draw(SCREEN)
      elif self.character is not False:
          for button in self.character_buttons:
              button.draw(SCREEN)

class Button:
  def __init__(self, x, y, width, height, text, color, hover_color, text_color, font_size, action=None):
    self.rect = pygame.Rect(x, y, width, height)
    self.color = color
    self.hover_color = hover_color
    self.text_color = text_color
    self.font = pygame.font.Font(None, font_size)
    self.message = text
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
        
class Banner:
  def __init__(self, x, color):
    self.x = x
    self.color = color
    self.font = pygame.font.Font(None, 30)  # Font size 30
    self.message = ''  # Placeholder for the message
  
  def set_text(self, text): 
    self.message = text

  def set_color(self, color): 
    self.color = color

  def draw(self, SCREEN):
    text_surface = self.font.render(self.message, True, self.color)
    
    rect = text_surface.get_rect()
    rect.centerx = SCREEN.get_rect().centerx 
    rect.top = self.x  

    SCREEN.blit(text_surface, rect)


