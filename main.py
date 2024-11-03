import pygame
from scenes.scene_manager import SceneManager
from state.grid_state import State

pygame.init()
screen = pygame.display.set_mode((800, 600))

grid_state = State()

manager = SceneManager(screen, grid_state)
manager.run()
pygame.quit()

