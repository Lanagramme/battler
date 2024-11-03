import pygame
from grid import Pion
from utils.constants import SCREEN
from utils.colors import colors
pygame.font.init()

class Game:
  def __init__(self, grid):
    self.grid = grid
    self.clicking = False
    self.playing = True


  def setup(self, team, type, coord, character ):
    if type == "random":
      while True:
        X = randrange(coord[0])
        Y = randrange(coord[1])
        nouveau_pion = Pion(team, (X, Y), character)
        if self.grid.get_pion(x,y) == None:
          break
    else:
      nouveau_pion =  Pion(team, coord, character)
      X, Y = coord
    self.grid.cells[X][Y].pion = len(self.LIST_PIONS)
    self.LIST_PIONS.append(nouveau_pion)
    self.TEAMS[team]["pions"].append(nouveau_pion)

  def run(self):
    while self.playing:
      self.handle_events()
      self.render()
      pygame.display.flip()

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.playing = False

      # if battle.attacking:
      #   for button in ui.attack_buttons:
      #     button.handle_event(event)
      # elif battle.moving:
      #     ui.cancel_btn.handle_event(event)
      # else:
      #   for button in ui.character_buttons:
      #     button.handle_event(event)
      # ui.turn_button.handle_event(event)

    mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
    clic, _, _ = pygame.mouse.get_pressed(num_buttons=3)

    if not clic:
      self.clicking = False

    if self.grid.board.collidepoint(mouse_pos):
      self.grid.hover = self.grid.get_hovered_cell(mouse_x, mouse_y)
      x, y = self.grid.hover
      hover_cell = self.grid.cells[x][y]
      
      # hover_pion = battle.LIST_PIONS[hover_cell.pion] if hover_cell.pion != None else None
      
      # if hover_cell.area == 'attack':
      #   if Spells[battle.active_spell][ "prevision_aoe" ]:
          # aoe(hover_cell, "prev", Spells[battle.active_spell][ "prevision_aoe" ], "circle")
      # else:
      #   clean_prev()
        
      if clic and not self.clicking:
        self.clicking = True
        
        
        # if hover_cell.area == "attack":
        #   if Spells[battle.active_spell]:
        #     Spells[battle.active_spell]["effect"](hover_cell)
        #   battle.attacking = False
        #   ui.cancel_menu()
        #   return
        # if hover_pion is not None and hover_pion.team == battle.turn:
        #   grid.activate(x, y, battle)
        #   battle.moving = False
        #
        # elif hover_pion is None:
        #   if hover_cell.area == "move":
        #     battle.LIST_PIONS[grid.active.pion].move(grid.cells[x][y])
        #   else : 
        #     clean_aoe()
        #     clean_active()
    else:
      self.grid.hover = (None, None)
      if clic and not self.clicking:
        self.clicking = True

  def render(self):
    SCREEN.fill(colors.WHITE)
    self.grid.paint(SCREEN)
    # ui.draw()
