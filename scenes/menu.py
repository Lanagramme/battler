import pygame
from classes.scene import Scene

class MenuScene(Scene):
  def __init__(self):
      super().__init__()
      self.font = pygame.font.Font(None, 50)
      self.bigfont = pygame.font.Font(None, 200)
      self.smallfont = pygame.font.Font(None, 30)

  def handle_events(self, events):
      for event in events:
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_RETURN:  # Press Enter to start game
                  return 'game'  # Return the name of the next scene

  def render(self, screen):
      screen.fill((30, 30, 30))  # Dark background
      name = self.smallfont.render('Beyond the Veil', True, (255, 255, 255))
      name_rect = name.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    
      title = self.bigfont.render('BATTLER', True, (255, 255, 255))
      title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
      text = self.font.render('Press Enter to Start', True, (255, 255, 255))
      text_rect = text.get_rect(center=(screen.get_width() // 2, (screen.get_height() // 3 )*2))
    
      screen.blit(text, text_rect)
      screen.blit(title, title_rect)
      screen.blit(name, name_rect)
