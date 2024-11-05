import pygame
from data.spells import Spells
from utils.colors import colors
from classes.grid import Pion
from classes.character import Character
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
    print(self.TEAMS[self.turn][ "pions" ])
    for pion in self.TEAMS[self.turn][ "pions" ]:
      if pion.character:
        if pion.character.hp > 0:
          pion.character.moves = pion.character.max_moves
    self.change_turn = True


  def setup(self, team):
    for i, member in enumerate(team):
      match i:
        case 0:
          coord = (2, 2)
        case 1:
          coord = (2, 4)
        case 2:
          coord = (2, 6)
      pion = Pion("Team 1", coord, member)
      self.LIST_PIONS.append(pion)
      self.TEAMS["Team 1"]["pions"].append(pion)
    spells = [Spells["Fireball"], Spells['Water stream']]
    Demo  = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40, 5)
    Demo2 = Demo
    Demo3 = Demo
    Demo2.name = "Demo 2"
    Demo3.name = "Demo 3"
    team2 = [Demo, Demo2, Demo3]
    for i, char in enumerate(team2):
      match i:
        case 0:
          coord = (10, 2)
        case 1:
          coord = (10, 4)
        case 2:
          coord = (10, 6)
      pion = Pion("Team 2", coord, char)
      self.LIST_PIONS.append(pion)
      self.TEAMS['Team 2']["pions"].append(pion) 
