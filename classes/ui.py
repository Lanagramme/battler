import pygame
pygame.font.init()
from utils.colors import colors
from utils.constants import HEIGHT, WIDTH, SCREEN, MARGIN

from classes.ui_components import Button, Banner, Fade, TurnBanner


    
class Ui:
  def __init__(self, WIDTH, HEIGHT, game_state):
    self.game_state = game_state
    self.game_state.add_observer(self)
    self.turn_display = Banner(15, colors.BLACK)  # UI component for turn display
    
    self.font  = pygame.font.Font("./assets/regular.ttf", 15)
    self.Hfont = pygame.font.Font("./assets/rounded.ttf", 17)
    self.Bfont = pygame.font.Font("./assets/regular.ttf", 15)
    self.set_turn()
    
    self.turn_banner = TurnBanner(self.game_state)
    
    self.clear_aoe = False
    self.character = False
    self.turn_button = Button(
      WIDTH-15-100, 15, 
      100, 35, 
      "Turn", 
      colors.BLUE, 
      colors.DARK_BLUE, 
      colors.BLACK, 25, action=self.game_state.next_turn)
    self.character_buttons = []
    self.attack_buttons = []

    self.infos = []

    self.char_anchor = {
      "y" : HEIGHT - MARGIN["bottom"] -18,
      "x" : 10
    }
    self.anchor = pygame.Rect(self.char_anchor["x"], self.char_anchor['y'], 400, MARGIN['bottom'])
    self.cancel_btn = Button(230, self.char_anchor['y'] + 15, 100, 35, "Cancel", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 25, action=lambda: self.cancel_menu(game_state))

  def update(self, event, *args):
    """React to state changes."""
    if event == "TURN_CHANGED":
      new_turn, turn_number = args
      self.turn_display.set_text(f"Turn: {new_turn} ({turn_number})")
      self.turn_display.set_color(self.game_state.TEAMS[new_turn]["color"])
      
  def character_info(self, x, y, color, info):
    fade = Fade(x, y, color, info)
    self.infos.append(fade)
    
  def set_turn(self):
    self.current_turn = Banner(15, colors.BLACK) 
    self.current_turn.set_text(self.game_state.turn)
    self.current_turn.set_color(self.game_state.active_team["color"])

  def cancel_menu(self, game_state):
    self.clear_aoe = True
    game_state.moving = False
    game_state.attacking = False

  def set_character(self, character, game_state, grid, ):
    self.character_buttons.clear()
    self.attack_buttons.clear()
    # elements = []
    elements = {}

    height = grid.spanY + 105
    margin = grid.margin['left']
    
    self.add_character_info(elements, character, margin, height, )
    self.create_character_buttons(game_state, grid)
    self.create_spell_buttons(character, game_state, grid)
    self.attack_buttons.append(self.cancel_btn)
    # self.character = elements
    self.character = character

  def add_character_info(self, elements, character, margin, height, ):
    name = self.Hfont.render(character.name, True, colors.BLACK)
    hp = self.font.render(f"{character.hp}/{character.max_hp}", True, colors.BLACK)
    move_info = self.font.render(f"Mp: {character.mp}/{character.max_mp}", True, colors.BLACK)
  
  def create_character_buttons(self, game_state, grid):
    pos_y = self.char_anchor['y'] + 15
    bas_x = 230
 
    width= 100
    height= 35
 
    move    = Button(bas_x, pos_y, width, height, "Move", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 25, action=grid.aoe_move)
    attack  = Button(bas_x + width +10, pos_y, width, height, "Attack", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 25, action=grid.aoe_attack)
  
    self.character_buttons.append(move)
    self.character_buttons.append(attack)

  def create_spell_buttons(self, character, game_state, grid):
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
    for pion in self.game_state.LIST_PIONS:
      if pion.character.name == character.name:
        true_character = pion.character
        break

    if not true_character:
      self.character = False
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
    offset_x = 65 + portrait_rayon*2
    offset_y = 50
    
    token_rayon = 18
    aura_rayon  = 10
    token_width = token_rayon * 2
    
    def draw_token(color, element):
      token_positions = {
        "earth" :     (offset_x, y + offset_y),
        "water" :     (offset_x + token_width, y + offset_y),
        "fire" :      (offset_x, y + offset_y + token_width),
        "neutral" :   (offset_x + token_width, y + offset_y + token_width),
      }
      
      aura_positions = {
        "earth" :     (offset_x - 18, y + offset_y + 5),
        "water" :     (offset_x + token_width + 18, y + offset_y + 5),
        "fire" :      (offset_x - 18, y + offset_y + token_width + 5),
        "neutral" :   (offset_x + token_width + 18, y + offset_y + token_width + 5),
      }
      
      token = pygame.draw.circle(SCREEN, color, token_positions[element] , token_rayon )
      token_value = self.font.render(str(character.tokens[element]), True, colors.BLACK)
      token_value_rect = token_value.get_rect(center=token.center)
      SCREEN.blit(token_value,token_value_rect)

      aura = pygame.draw.circle(SCREEN, color, aura_positions[element] , aura_rayon )
      aura_border = pygame.draw.circle(SCREEN, colors.BLACK, aura_positions[element] , aura_rayon, 1 )
      aura_value = self.font.render(str(character.aura[element]), True, colors.BLACK)
      aura_value_rect = aura_value.get_rect(center=aura.center)
      aura_border_rect = aura_value.get_rect(center=aura.center)
      SCREEN.blit(aura_value,aura_value_rect)
      
    draw_token(colors.BLUE  , "water"   )
    draw_token(colors.GREEN , "earth"   )
    draw_token(colors.RED   , "fire"    )
    draw_token(colors.ORANGE, "neutral" )

  def draw(self, SCREEN):
    self.current_turn.draw(SCREEN)
    self.turn_button.draw(SCREEN)
    
    self.turn_banner.draw(SCREEN)
    
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
    if self.game_state.attacking:
        for button in self.attack_buttons:
            button.draw(SCREEN)
    elif self.game_state.moving:
        print('movin')
        self.cancel_btn.draw(SCREEN)
    elif self.character is not False:
        for button in self.character_buttons:
            button.draw(SCREEN)

            
