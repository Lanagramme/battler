from utils.colors import colors
import pygame
def fade_to_black(screen, duration=500):
  """Fade the screen to black over a given duration (in milliseconds)."""
  fade_surface = pygame.Surface(screen.get_size())
  fade_surface.fill((0, 0, 0))
  
  for alpha in range(0, 255, 5):  # Adjust step size for speed
      fade_surface.set_alpha(alpha)  # Set transparency
      screen.blit(fade_surface, (0, 0))  # Draw the fade surface
      pygame.display.flip()
      pygame.time.delay(duration // 51)  # Total time divided by number of frames (51 in this case)


def fade_out_surface(screen, turn, color, fade_speed=3):
    center_surface = pygame.Surface((500, 200), pygame.SRCALPHA)
    center_surface.fill(color)
    font = pygame.font.Font(None, 100)
    turn = font.render(turn, True, colors.BLACK)
    turn_surface = turn.get_rect(center=screen.get_rect().center)

    center_rect = center_surface.get_rect(center=screen.get_rect().center)

    alpha = 255

    def fade_step():
        nonlocal alpha  # Reference the alpha value in the outer scope
        if alpha > 0:
            alpha -= fade_speed  # Decrease alpha to make the surface more transparent
            screen.blit(turn, turn_surface)
            if alpha < 0:
                alpha = 0
            center_surface.set_alpha(alpha)  # Apply alpha transparency
        
        screen.blit(center_surface, center_rect)
    
    return fade_step
