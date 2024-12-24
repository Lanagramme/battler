import pygame
pygame.font.init()
from utils.colors import colors
from utils.constants import HEIGHT, WIDTH, SCREEN, MARGIN

class Fade:
  def __init__(self, x, y, color, info):
    self.x = x
    self.y = y
    self.font = pygame.font.Font(None, 30)
    self.popup = self.font.render(info, True, color )
    self.alpha = 255
    self.fade_speed = 2

  def update(self):
    self.popup.set_alpha(self.alpha)
    if self.alpha > 0:
      self.alpha -= self.fade_speed
      self.x -= 5
      if self.alpha < 0:
        self.alpha = 0
    SCREEN.blit(self.popup, (self.x, self.y))
    pygame.display.flip()
    
class Ui:
  def __init__(self, WIDTH, HEIGHT, battle):
    self.font  = pygame.font.Font("./assets/regular.ttf", 15)
    self.Hfont = pygame.font.Font("./assets/rounded.ttf", 17)
    self.Bfont = pygame.font.Font("./assets/regular.ttf", 15)
    self.battle = battle
    self.set_turn()
    self.clear_aoe = False
    self.character = False
    self.turn_button = Button(
      WIDTH-15-100, 15, 
      100, 35, 
      "Turn", 
      colors.BLUE, 
      colors.DARK_BLUE, 
      colors.BLACK, 25, action=self.battle.next_turn)
    self.character_buttons = []
    self.attack_buttons = []

    self.infos = []

    self.char_anchor = {
      "y" : HEIGHT - MARGIN["bottom"] -18,
      "x" : 10
    }
    self.anchor = pygame.Rect(self.char_anchor["x"], self.char_anchor['y'], 400, MARGIN['bottom'])
    self.cancel_btn = Button(230, self.char_anchor['y'] + 15, 100, 35, "Cancel", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 25, action=lambda: self.cancel_menu(battle))

  def character_info(self, x, y, color, info):
    fade = Fade(x, y, color, info)
    self.infos.append(fade)
    
  def set_turn(self):
    self.current_turn = Banner(15, colors.BLACK) 
    self.current_turn.set_text(self.battle.turn)
    self.current_turn.set_color(self.battle.active_team["color"])

  def cancel_menu(self, battle):
    self.clear_aoe = True
    battle.moving = False
    battle.attacking = False

  def set_character(self, character, battle, grid, ):
    self.character_buttons.clear()
    self.attack_buttons.clear()
    # elements = []
    elements = {}

    height = grid.spanY + 105
    margin = grid.margin['left']
    
    self.add_character_info(elements, character, margin, height, )
    self.create_character_buttons(battle, grid)
    self.create_spell_buttons(character, battle, grid)
    self.attack_buttons.append(self.cancel_btn)
    # self.character = elements
    self.character = character

  def add_character_info(self, elements, character, margin, height, ):
    name = self.Hfont.render(character.name, True, colors.BLACK)
    hp = self.font.render(f"{character.hp}/{character.max_hp}", True, colors.BLACK)
    move_info = self.font.render(f"Mp: {character.mp}/{character.max_mp}", True, colors.BLACK)
  
  def create_character_buttons(self, battle, grid):
    pos_y = self.char_anchor['y'] + 15
    bas_x = 230
 
    width= 100
    height= 35
 
    move    = Button(bas_x, pos_y, width, height, "Move", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 25, action=grid.aoe_move)
    attack  = Button(bas_x + width +10, pos_y, width, height, "Attack", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 25, action=grid.aoe_attack)
  
    self.character_buttons.append(move)
    self.character_buttons.append(attack)

  def create_spell_buttons(self, character, battle, grid):
    pos_y = self.char_anchor['y'] + 15
    bas_x = 230
    
    for i, spell in enumerate(character.spells):
      x = bas_x + (i + 1) * (100 + 15) 
      y = pos_y
      width, height = (100, 35)
      btn = Button(
        x, y, 
        width, height,
        spell.name, 
        colors.BLUE, 
        colors.DARK_BLUE, 
        colors.BLACK, 25,
        action=lambda spell=spell: grid.draw_aoe_from_caster(spell)
      )
      self.attack_buttons.append(btn)

  def create_token_ui(self, character, x, y):
    true_character = False
    for pion in self.battle.LIST_PIONS:
      if pion.character.name == character.name:
        true_character = pion.character
        break

    if not true_character:
      print("ERROR => character not found")
      return
    
    pygame.draw.rect(SCREEN, colors.BLACK, self.anchor , 1)
    
    # draw portrait
    portrait_rayon = (MARGIN['bottom'] )/2
    portrait_x = x + 20 + portrait_rayon
    portrait_y = y + portrait_rayon
    portrait = pygame.draw.circle(SCREEN,colors.BLACK, (portrait_x , portrait_y) , portrait_rayon ,1)

    move_info = self.font.render(f"Mp: {character.mp}/{character.max_mp}", True, colors.BLACK)
    
    # draw name
    name_w = (portrait_rayon * 2) - 8
    name_h = 20
    name_x = portrait.center[0] - portrait_rayon + 4
    name_y = portrait.center[1] + portrait_rayon - name_h/2
    name_detail = ((name_x, name_y),(name_w, 20))
    pygame.draw.rect(SCREEN, colors.WHITE, name_detail, 0, 5)
    name_square = pygame.draw.rect(SCREEN, colors.BLACK, name_detail, 1, 5)
    name = self.Hfont.render(character.name, True, colors.BLACK)
    name_rect = name.get_rect(center=name_square.center)
    SCREEN.blit(name, name_rect)
    
    # draw HP
    hp = self.font.render(f"{character.hp}/{character.max_hp}", True, colors.BLACK)
    hp_rect = hp.get_rect(center=(portrait.center[0],portrait.center[1] + portrait_rayon - 20))
    SCREEN.blit(hp, hp_rect)
    
    # draw tokens
    y = y-5 
    offset_x = 50 + portrait_rayon*2
    offset_y = 50
    
    token_rayon = 18
    token_width = token_rayon * 2
    
    def draw_token(color, element):
      positions = {
        "earth" :     (offset_x, y + offset_y),
        "water" :     (offset_x + token_width, y + offset_y),
        "fire" :      (offset_x, y + offset_y + token_width),
        "neutral" :   (offset_x + token_width, y + offset_y + token_width),
      }
      
      token = pygame.draw.circle(SCREEN, color, positions[element] , token_rayon )
      token_value = self.font.render(str(character.tokens[element]), True, colors.BLACK)
      token_value_rect = token_value.get_rect(center=token.center)
      SCREEN.blit(token_value,token_value_rect)

    draw_token(colors.BLUE  , "water"   )
    draw_token(colors.GREEN , "earth"   )
    draw_token(colors.RED   , "fire"    )
    draw_token(colors.ORANGE, "neutral" )

  def draw(self, SCREEN):
    self.current_turn.draw(SCREEN)
    self.turn_button.draw(SCREEN)
    if self.character:
      x, y, = (self.char_anchor["x"], self.char_anchor["y"])
      # for element in self.character:
      #   SCREEN.blit(element[0], element[1])
      self.draw_buttons(SCREEN)
      self.create_token_ui(self.character, x, y)

    for info in self.infos[:]:
      info.update()
      if info.alpha == 0:
        self.infos.remove(info)

  def draw_buttons(self, SCREEN):
    if self.battle.attacking:
        for button in self.attack_buttons:
            button.draw(SCREEN)
    elif self.battle.moving:
        print('movin')
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
    # self.font = pygame.font.Font(None, font_size)
    self.font = pygame.font.Font("./assets/rounded.ttf", font_size)
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

