import pygame
from data.spells import Spells

from utils.colors import colors
from utils.constants import SCREEN
from utils.functions import fade_out_surface

from classes.grid import Pion
from classes.character import Character

pygame.font.init()

class State():
  def __init__(self):
    self.turn = 'Team 1'
    self.turn_number = 1
    self.LIST_PIONS = []
    self.TEAMS = {
      "Team 1": {"color": colors.PURPLE, "pions": []},
      "Team 2": {"color": colors.CARMIN, "pions": []},
    }
    self.active_team = self.TEAMS[self.turn]
    self.moving = False
    self.attacking = False
    self.active_spell = False
    self.change_turn = False
    self.fade_turn_pannel = fade_out_surface(SCREEN, 'Team 1', self.TEAMS[self.turn]["color"])

  def next_turn(self):
    self.turn = "Team 2" if self.turn == "Team 1" else "Team 1"
    if self.turn == "Team 1": self.turn_number += 1
    self.fade_turn_pannel = fade_out_surface(SCREEN, self.turn, self.TEAMS[self.turn]["color"])
    for pion in self.TEAMS[self.turn][ "pions" ]:
      if pion.character:
        if pion.character.hp > 0:
          pion.character.mp = pion.character.max_mp
          pion.character.turn_reset(self.turn_number)
    self.change_turn = True
    self.active_team = self.TEAMS[self.turn]

  def setup(self, team, team2):
    for i, member in enumerate(team):
      match i:
        case 0: coord = (2, 2)
        case 1: coord = (2, 4)
        case 2: coord = (2, 6)
      pion = Pion("Team 1", coord, member)
      self.LIST_PIONS.append(pion)
      self.TEAMS["Team 1"]["pions"].append(pion)
    
    for i, char in enumerate(team2):
      match i:
        case 0: coord = (10, 2)
        case 1: coord = (10, 4)
        case 2: coord = (10, 6)
      pion = Pion("Team 2", coord, char)
      self.LIST_PIONS.append(pion)
      self.TEAMS['Team 2']["pions"].append(pion) 
