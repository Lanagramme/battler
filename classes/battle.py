import pygame
from utils.colors import colors
from grid import Pion
pygame.font.init()


class Battle:
  def __init__(self ):
    self.turn = 'Team 1'
    self.LIST_PIONS = []
    self.TEAMS = {
      "Team 1": {"color": colors.PURPLE, "pions": []},
      "Team 2": {"color": colors.CARMIN, "pions": []},
    }
    self.moving = False
    self.attacking = False
    self.active_spell = False

  def next_turn(self):
    self.turn = "Team 2" if self.turn == "Team 1" else "Team 1"
    for pion in self.TEAMS[self.turn][ "pions" ]:
      pion.character.moves = pion.character.max_moves
#   ui.current_turn.set_text(self.turn)
#   ui.current_turn.set_color(self.TEAMS[self.turn]["color"])
#   clean_active()
#   clean_aoe()
  
  # create a pion for the battle and automatically attribute to a team
  def create(self, team, type, coord, character, grid):
    if type == "random":
      while True:
        X = randrange(coord[0])
        Y = randrange(coord[1])
        nouveau_pion = Pion(team, (X, Y), character)
        if grid.cells[X][Y].pion == None:
          break
    else:
      nouveau_pion =  Pion(team, coord, character)
      X, Y = coord
    grid.cells[X][Y].pion = len(self.LIST_PIONS)
    self.LIST_PIONS.append(nouveau_pion)
    self.TEAMS[team]["pions"].append(nouveau_pion)

  # def start(self, GX, GY):
  #   ui.current_turn.set_text(self.turn)
  #   ui.current_turn.set_color(self.TEAMS[self.turn]["color"])
