import pygame
from utils.colors import colors
from utils.constants import HEIGHT, WIDTH, SCREEN, MARGIN
from patterns.observer import Observer

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
    self.action = action
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

class ActionButton(Button):
  def __init__(self, x, y, text, action):
    super().__init__(x, y, 100, 35, text, colors.BLUE, colors.DARK_BLUE, colors.BLACK, 25, action)

        
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

class TurnBanner(Observer):
  def __init__(self, game_state):
    """Initialize TurnBanner as an observer of game_state"""
    self.game_state = game_state
    self.game_state.add_observer(self)  # Register as an observer
    
    self.font = pygame.font.Font(None, 80)
    self.banner_surface = None
    self.text_surface = None
    self.visible = False  # Is the banner currently active?
    self.timer = 60  # Time to stay visible (1 second at 60 FPS)
    self.speed = 15  # Speed of sliding effect

    # Banner position (starts off-screen)
    self.start_y = -100  # Above the screen
    self.target_y = SCREEN.get_height() // 4  # Final position when sliding in
    self.current_y = self.start_y  # Current Y position
    self.direction = 'down'

    self.update_surface()  # Pre-generate surfaces

  def update(self, event, *args):
    """Triggered when the turn changes."""
    if event == "TURN_CHANGED":
      self.current_y = self.start_y  # Reset to off-screen position
      self.timer = 60  # Stay visible for 1 second (60 frames at 60 FPS)
      self.visible = True  # Activate the banner
      self.update_surface()  # Refresh text and color

  def update_surface(self):
      """Creates the banner's surfaces only when needed."""
      color = self.game_state.TEAMS[self.game_state.turn]["color"]
      self.banner_surface = pygame.Surface((500, 100), pygame.SRCALPHA)
      self.banner_surface.fill(color)

      message = f"Turn: {self.game_state.turn}"
      self.text_surface = self.font.render(message, True, colors.BLACK)

  def draw(self, screen):
      """Handles slide in, wait, and slide out animation."""
      if not self.visible:
          return  # Skip drawing if not active

      # Slide in
      if self.current_y < self.target_y and self.direction == 'down':
          self.current_y += self.speed
          if self.current_y > self.target_y:  # Prevent overshooting
              self.current_y = self.target_y

      # Countdown for staying visible
      elif self.timer > 0:
        self.direction = "up"
        self.timer -= 1  # Countdown in frames (1 second at 60 FPS)

      # Slide out
      else:
          self.current_y -= self.speed
          if self.current_y <= self.start_y:  # Fully off-screen
              self.visible = False  # Hide banner

      # Center the banner horizontally
      banner_rect = self.banner_surface.get_rect(center=(SCREEN.get_width() // 2, self.current_y))
      text_rect = self.text_surface.get_rect(center=banner_rect.center)

      # Draw banner and text
      screen.blit(self.banner_surface, banner_rect)
      screen.blit(self.text_surface, text_rect)
