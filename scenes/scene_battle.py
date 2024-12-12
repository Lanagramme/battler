import pygame
from classes.scene import Scene
from classes.ui import Ui
from data.spells import Spells
from utils.colors import colors

class BattleScene(Scene):
  def __init__(self, state):
    super().__init__()
    self.grid = None
    self.battle = state
    self.clicking = False
    self.actor = False

  # Handles player input and updates game state based on events.

  # Mouse Handling:
  # * Hover Mechanics:
      # When the mouse hovers over the grid, detects the hovered cell and pion  
      # If hovering over an "attack" area, calculates and displays AoE using the spell's configuration.
  # * Click Handling:
      # Executes attacks if in an "attack" area, applying spell effects and damage. 
      # Handles movement logic when clicking on a "move" area.
      # Clears AoE indicators and active cells when clicking elsewhere.
      
  # Dead characters are removed from the grid.

  def handle_events(self, events):
    attack_in_progress = self.battle.attacking

    # handle ui buttons
    for event in events:
      if attack_in_progress:
        for button in self.ui.attack_buttons:
          button.handle_event(event)
      elif self.battle.moving:
        self.ui.cancel_btn.handle_event(event)
      else:
        for button in self.ui.character_buttons:
          button.handle_event(event)
      self.ui.turn_button.handle_event(event)
      
    # handle the mouse clic
    mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
    clic, _, _ = pygame.mouse.get_pressed(num_buttons=3)
    if not clic:
      self.clicking = False

    # if the mouse hovers the grid
    if self.grid.board.collidepoint(mouse_pos):
      self.grid.hover = self.grid.get_hovered_cell(mouse_x, mouse_y)
      x, y = self.grid.hover
      hover_cell = self.grid.cells[x][y]
      hover_pion = hover_cell.pion if hover_cell.pion != None else None

      # draw the spell aoe if the mouse hovers the spell range
      if hover_cell.area == 'attack':
        active_spell = Spells[self.battle.active_spell]
        if active_spell[ "prevision_aoe" ]:
          self.grid.draw_aoe(hover_cell, "prev", active_spell[ "prevision_aoe" ], active_spell["prevision_type"])
      else:
        self.grid.clean_prev()

      # handle clic events on the grid
      if clic and not self.clicking:
        self.clicking = True

        if hover_cell.area == "attack":
          if active_spell:
            # add all targets in the spell's aoe
            if len(self.grid.prevision_aoe):
              target = []
              for cell in self.grid.prevision_aoe:
                target.append(cell)
            else:
              target = [hover_cell]
             
            # apply spell effect and damage
            active_spell["effect"](target, self.grid)
            damage = active_spell["damage"]

            # update character ui
            for cell in target:
              if cell.pion:
                self.ui.character_info(cell.y, cell.y, colors.RED, "-"+str(damage))
                # kill dead characters
                if cell.pion.character.hp <= 0:
                  cell.pion.character = False
                  cell.pion = None
                
          attack_in_progress = False
          self.ui.cancel_menu(self.battle)
          return

        # select active pion
        if hover_pion is not None and hover_pion.team == self.battle.turn:
          self.grid.activate(x, y, )
        
        elif hover_pion is None:
          if hover_cell.area == "move":
            self.grid.active.pion.move(self.grid.get_cell(x,y), self.grid)
          else : 
            self.grid.clean_aoe()
            self.grid.clean_active()
    else:
      self.grid.hover = (None, None)
      if clic and not self.clicking:
        self.clicking = True
        

  def update(self):
    # change turn
    if self.battle.change_turn == True:
      self.next_turn()
    # clean aoe 
    if self.ui.clear_aoe:
      self.grid.clean_aoe()
      self.ui.clear_aoe = False
    # set/clean ui
    if self.grid.active :
      if self.grid.active.pion:
        self.ui.set_character( self.grid.active.pion.character, self.battle, self.grid)
      else:
        self.grid.clean_active()
    else:
      self.ui.character = False

  def render(self, screen):
    screen.fill(colors.WHITE)
    self.grid.paint(screen)
    self.ui.draw(screen)
    self.ui.draw_buttons(screen)
    self.battle.fade_turn_pannel()

  def next_turn(self):
    self.ui.set_turn(self.battle.turn)
    self.grid.clean_active()
    self.grid.clean_aoe()
    self.battle.change_turn = False
