import pygame
from random import randrange
from utils.colors import colors
from character import Character
from ui import Banner, Ui
from constants import SIZE, SCREEN, pygame
from battle import Battle

from grid import grid

# Classes
from character import Character
from game import Game
from game_state import State

pygame.init()
pygame.font.init()
pygame.display.set_caption("Battler")
pygame.time.Clock().tick(60)


# state = State()

# def Spell(name, reach, aoe, damage, prevision=False):
#   return {
#     'name': name, "range":reach, 'aoe': aoe, 'damage': damage, "prevision_aoe": prevision
#   }
#
#
# def neighbors(cell):
#     directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#     newarea = set()
#
#     for dx, dy in directions:
#         nx, ny = cell.x + dx, cell.y + dy
#         if 0 <= nx < grid.X and 0 <= ny < grid.Y:
#             newarea.add(grid.cells[nx][ny])
#     
#     return newarea
#
# battle = Battle()
#
# Spells = {}
#
# def direct_damage(spell, targets):
#   for target in targets:
#     if target.pion is not None:
#       battle.LIST_PIONS[target.pion].loose_pv(spell['damage'])
#
# def get_spell_targets(spell):
#   targets
#   for cell in grid.attack_aoe:
#     if cell.pion is not False:
#       targets.append(cell)
#   return targets
#
# Spells["Fireball"] = Spell('Fireball', 8, "circle", 3, False)
#
# def fireball_effect(target):
#   spell = Spells['Fireball']
#   direct_damage(Spells['Fireball'], [ target ])
#
# Spells['Fireball']["effect"] = fireball_effect
#
# Spells['Water stream'] = Spell('Water stream', 4, "line", 3, 3)
#  
# def water_stream_effect(target):
#   spell = Spells['Water stream']
#   direct_damage(spell, [ target ])
#
# Spells['Water stream']["effect"] = water_stream_effect
#
# spells = [Spells["Water stream"],  Spells['Fireball']]
#
# # Characters
# Lance = Character('Lance', 12, 4, 5, './sprite_sheet/silver.png', spells, ["bottom", "left", "right", "top"], 60, 60)
# Touko = Character('Touko', 2, 4, 4, './sprite_sheet/past.png', spells, ["bottom", "left", "right", "top"], 60, 60)
# Azure = Character('Azure', 12, 4, 3, './sprite_sheet/azure.jpg', spells, ["bottom", "left", "right", "top"], 60, 60)
# Girl  = Character('Girl', 2, 4, 3, './sprite_sheet/girl.png', spells, ["bottom", "left", "right", "top"], 60, 60)
# Demo  = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40)
# Demo1 = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40)
Demo2 = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', [], ["bottom", "left", "right", "top"], 34, 40)
# Demo2 = Character('Demo', 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40)
#
battle = Battle()
# battle.create('Team 2', "fix", (11, 2), Demo2, grid)
# battle.create('Team 2', "fix", (11, 4), Demo2, grid)
# battle.create('Team 2', "fix", (11, 6), Demo1, grid)
# # battle.create('Team 1', "random", ( 3,grid.Y ) , Girl)
# # battle.create('Team 1', "random", ( 3,grid.Y ) , Lance)
# # battle.create('Team 1', "random", ( 3,grid.Y ) , Touko)
# battle.create('Team 1', "fix", ( 2,2) , Girl, grid)
# battle.create('Team 1', "fix", ( 2,4 ) , Lance, grid)
# battle.create('Team 1', "fix", ( 2,6 ) , Touko, grid)
# battle.start(grid.X, grid.Y)
#
# current_turn = Banner(15,colors.BLACK)
# ui = Ui(current_turn, WIDTH, HEIGHT, battle)

game = Game(grid)
game.run()
