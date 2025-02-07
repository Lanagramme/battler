import pygame
from utils.colors import colors
from utils.constants import HEIGHT, WIDTH, SCREEN, MARGIN
from patterns.observer import Observer  # Correct Import

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
        if self.current_y < self.target_y:
            self.current_y += self.speed
            if self.current_y > self.target_y:  # Prevent overshooting
                self.current_y = self.target_y

        # Countdown for staying visible
        elif self.timer > 0:
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

    def __init__(self, game_state):
        self.game_state = game_state
        self.game_state.add_observer(self)  # Register as an observer
        
        self.font = pygame.font.Font(None, 80)
        self.banner_surface = None
        self.text_surface = None
        self.visible = False  # Is the banner currently active?
        self.timer = 0  # Time to stay visible before sliding out
        self.speed = 15  # Speed of sliding effect

        # Banner position (starts off-screen)
        self.start_y = -100  # Above the screen
        self.target_y = SCREEN.get_height() // 4  # Final position when sliding in
        self.current_y = self.start_y  # Current Y position

        self.update_surface()  # Pre-generate surfaces

    def update(self, event, *args):
        """Triggered when the turn changes."""
        if event == "TURN_CHANGED":
            self.current_y = self.start_y  # Reset to off-screen position
            self.timer = 60  # Stay visible for 1 second (60 frames at 60FPS)
            self.visible = True  # Activate the banner
            self.update_surface()  # Refresh text and color

    def update_surface(self):
        """Creates the banner's surfaces only when needed."""
        color = self.game_state.TEAMS[self.game_state.turn]["color"]
        self.banner_surface = pygame.Surface((500, 100), pygame.SRCALPHA)
        self.banner_surface.fill(color)

        message = f"{self.game_state.turn}"
        self.text_surface = self.font.render(message, True, colors.BLACK)

    def draw(self, screen):
        """Handles slide in, wait, and slide out animation."""
        if not self.visible:
            return  # Skip drawing if not active

        # Slide in
        if self.current_y < self.target_y:
            self.current_y += self.speed
            if self.current_y > self.target_y:  # Prevent overshooting
                self.current_y = self.target_y

        # Countdown for staying visible
        elif self.timer > 0:
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

    def __init__(self, game_state):
        self.game_state = game_state
        self.game_state.add_observer(self)  # Register as an observer
        
        self.font = pygame.font.Font(None, 80)
        self.banner_surface = None
        self.text_surface = None
        self.visible = False  # Is the banner currently active?
        self.timer = 0  # Time to stay visible before sliding out
        self.speed = 15  # Speed of sliding effect

        # Banner position (starts off-screen)
        self.start_y = -100  # Above the screen
        self.target_y = SCREEN.get_height() // 4  # Final position when sliding in
        self.current_y = self.start_y  # Current Y position

        self.update_surface()  # Pre-generate surfaces

    def update(self, event, *args):
        """Triggered when the turn changes."""
        if event == "TURN_CHANGED":
            self.current_y = self.start_y  # Reset to off-screen position
            self.timer = 60  # Stay visible for 1 second (60 frames at 60FPS)
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
        if self.current_y < self.target_y:
            self.current_y += self.speed
            if self.current_y > self.target_y:  # Prevent overshooting
                self.current_y = self.target_y

        # Countdown for staying visible
        elif self.timer > 0:
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

    def __init__(self, game_state):
        self.game_state = game_state
        self.game_state.add_observer(self)  # Register as an observer
        
        self.font = pygame.font.Font(None, 100)  
        self.alpha = 255  # Start fully visible
        self.fade_speed = 5  # Speed of fading
        
        self.banner_surface = None
        self.text_surface = None
        self.update_surface()  # Pre-generate surfaces

    def update(self, event, *args):
        """Triggered when the turn changes."""
        if event == "TURN_CHANGED":
            self.alpha = 255  # Reset fade effect
            self.update_surface()  # Recreate surfaces

    def update_surface(self):
        """Creates the surfaces only when a turn changes, reducing redundant rendering."""
        color = self.game_state.TEAMS[self.game_state.turn]["color"]
        self.banner_surface = pygame.Surface((500, 200), pygame.SRCALPHA)
        self.banner_surface.fill(color)

        message = f"Turn: {self.game_state.turn}"
        self.text_surface = self.font.render(message, True, colors.BLACK)

    def draw(self, SCREEN):
        """Draws and gradually fades the turn banner."""
        if self.alpha <= 0:
            return  # Skip rendering if fully faded

        # Apply fading effect
        self.banner_surface.set_alpha(self.alpha)
        self.text_surface.set_alpha(self.alpha)

        # Centered positions
        banner_rect = self.banner_surface.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
        text_rect = self.text_surface.get_rect(center=banner_rect.center)

        # Draw elements on the SCREEN
        SCREEN.blit(self.banner_surface, banner_rect)
        SCREEN.blit(self.text_surface, text_rect)

        # Reduce alpha (fade effect)
        self.alpha -= self.fade_speed

    def __init__(self, game_state):
        super().__init__()  # Initialize Observer
        self.game_state = game_state
        self.game_state.add_observer(self)  # Register as an observer
        
        self.font = pygame.font.Font(None, 100)  
        self.message = f"Turn: {self.game_state.turn}"  
        self.color = self.game_state.TEAMS[self.game_state.turn]["color"]
        
        self.alpha = 255  # Start fully visible
        self.fade_speed = 5  # Speed of fading
        self.active = True  # Determines whether the banner is visible
        
    def update(self, event, *args):
        """Triggered when the turn changes."""
        if event == "TURN_CHANGED":
            new_turn, turn_number = args
            self.message = f"Turn: {new_turn}"
            self.color = self.game_state.TEAMS[new_turn]["color"]
            self.alpha = 255  # Reset alpha to make the banner visible again
            self.active = True  # Reactivate the fade effect

    def draw(self, SCREEN):
        """Draws and gradually fades the turn banner."""
        if not self.active:
            return  # Don't draw if fully faded

        # Create surface with transparency
        banner_surface = pygame.Surface((500, 200), pygame.SRCALPHA)
        banner_surface.fill(self.color)
        banner_surface.set_alpha(self.alpha)  # Apply fade effect

        # Render text with fading effect
        text_surface = self.font.render(self.message, True, (0, 0, 0))  # Text in black
        text_surface.set_alpha(self.alpha)  # Apply the same alpha fading to the text

        # Get text position
        text_rect = text_surface.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))

        # Draw elements on the SCREEN
        SCREEN.blit(banner_surface, (SCREEN.get_width() // 2 - 250, SCREEN.get_height() // 2 - 100))
        SCREEN.blit(text_surface, text_rect)

        # Reduce alpha (fade effect)
        if self.alpha > 0:
            self.alpha -= self.fade_speed
        else:
            self.active = False  # Fully faded, deactivate

    def __init__(self, game_state):
        self.game_state = game_state
        self.game_state.add_observer(self)  # Register as an observer
        
        self.font = pygame.font.Font(None, 100)  
        self.message = f"Turn: {self.game_state.turn}"  
        self.color = self.game_state.TEAMS[self.game_state.turn]["color"]
        
        self.alpha = 255  # Start fully visible
        self.fade_speed = 5  # Speed of fading
        self.active = True  # Determines whether the banner is visible
        
    def update(self, event, *args):
        """Triggered when the turn changes."""
        if event == "TURN_CHANGED":
            new_turn, turn_number = args
            self.message = f"Turn: {new_turn}"
            self.color = self.game_state.TEAMS[new_turn]["color"]
            self.alpha = 255  # Reset alpha to make the banner visible again
            self.active = True  # Reactivate the fade effect

    def draw(self, SCREEN):
        """Draws and gradually fades the turn banner."""
        if not self.active:
            return  # Don't draw if fully faded
        
        # Create surface with transparency
        banner_surface = pygame.Surface((500, 200), pygame.SRCALPHA)
        banner_surface.fill(self.color)
        banner_surface.set_alpha(self.alpha)  # Apply fade effect
        
        # Render text
        text_surface = self.font.render(self.message, True, colors.BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
        
        # Draw elements on the SCREEN
        SCREEN.blit(banner_surface, (SCREEN.get_width() // 2 - 250, SCREEN.get_height() // 2 - 100))
        SCREEN.blit(text_surface, text_rect)
        
        # Reduce alpha (fade effect)
        if self.alpha > 0:
            self.alpha -= self.fade_speed
        else:
            self.active = False  # Fully faded, deactivate