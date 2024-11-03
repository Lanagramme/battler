import pygame
def fade_to_black(screen, duration=1000):
  """Fade the screen to black over a given duration (in milliseconds)."""
  fade_surface = pygame.Surface(screen.get_size())
  fade_surface.fill((0, 0, 0))
  
  for alpha in range(0, 255, 5):  # Adjust step size for speed
      fade_surface.set_alpha(alpha)  # Set transparency
      screen.blit(fade_surface, (0, 0))  # Draw the fade surface
      pygame.display.flip()
      pygame.time.delay(duration // 51)  # Total time divided by number of frames (51 in this case)
