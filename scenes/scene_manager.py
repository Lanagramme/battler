import pygame
from scenes.menu import MenuScene
from scenes.scene_battle import BattleScene
from scenes.scene_build_team import TeamSelect
from classes.ui import Ui
from classes.grid import Grid
from utils.functions import fade_to_black
from utils.constants import SIZE, SCREEN, HEIGHT, WIDTH, GUTTER, ROWS, COLLS, SIZE, CELL_SIZE, MARGIN

class SceneManager:
  def __init__(self, screen, battle_state):
    self.battle_state = battle_state
    self.screen = screen
    self.scenes = {
        'menu': MenuScene(),
        'game': TeamSelect(self.battle_state),
        'battle': BattleScene(self.battle_state),
    }
    self.current_scene = self.scenes['game']

  def switch_scene(self, new_scene_name):
    fade_to_black(self.screen)
    self.current_scene = self.scenes[new_scene_name]

    if new_scene_name == 'battle':
      self.scenes["battle"].grid = Grid(COLLS, ROWS, MARGIN, GUTTER, CELL_SIZE, self.battle_state)
      self.scenes['battle'].ui = Ui(self.battle_state.turn, WIDTH, HEIGHT, self.battle_state)

  def run(self):
    clock = pygame.time.Clock()
    running = True
    while running:
      events = pygame.event.get()
      for event in events:
        if event.type == pygame.QUIT:
          running = False
      
      next_scene = self.current_scene.handle_events(events)
      if next_scene:
        self.switch_scene(next_scene)

      self.current_scene.update()
      self.current_scene.render(self.screen)
  
      pygame.display.flip()
      clock.tick(60)
