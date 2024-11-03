import pygame
from utils.colors import colors
from classes.grid import Pion
pygame.font.init()

class State():
  def __init__(self):
    self.turn = 'Team 1'
    self.LIST_PIONS = []
    self.TEAMS = {
      "Team 1": {"color": colors.PURPLE, "pions": []},
      "Team 2": {"color": colors.CARMIN, "pions": []},
    }
    self.moving = False
    self.attacking = False
    self.active_spell = False
    self.change_turn = False

  def next_turn(self):
    self.turn = "Team 2" if self.turn == "Team 1" else "Team 1"
    for pion in self.TEAMS[self.turn][ "pions" ]:
      if pion.character:
        if pion.character.hp > 0:
          pion.character.moves = pion.character.max_moves
    self.change_turn = True


  def setup(self, team):
    for i, member in enumerate(team):
      pion = Pion("Team 1", (0, i), member)
      self.LIST_PIONS.append(pion)
      self.TEAMS["Team 1"]["pions"].append(pion)
