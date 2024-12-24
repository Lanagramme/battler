import pygame
from scenes.scene_manager import SceneManager
from state.grid_state import State

pygame.init()

SceneManager(State()).run()

pygame.quit()
