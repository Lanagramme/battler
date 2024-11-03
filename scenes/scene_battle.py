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

  def handle_events(self, events):
    for event in events:
      if self.battle.attacking:
        for button in self.ui.attack_buttons:
          button.handle_event(event)
      elif self.battle.moving:
          self.ui.cancel_btn.handle_event(event)
      else:
        for button in self.ui.character_buttons:
          button.handle_event(event)
      self.ui.turn_button.handle_event(event)
      
    mouse_x, mouse_y = mouse_pos = pygame.mouse.get_pos()
    clic, _, _ = pygame.mouse.get_pressed(num_buttons=3)

    if not clic:
      self.clicking = False
      

    if self.grid.board.collidepoint(mouse_pos):
      self.grid.hover = self.grid.get_hovered_cell(mouse_x, mouse_y)
      x, y = self.grid.hover
      hover_cell = self.grid.cells[x][y]
      hover_pion = hover_cell.pion if hover_cell.pion != None else None

      if hover_cell.area == 'attack':
        if Spells[self.battle.active_spell][ "prevision_aoe" ]:
          self.grid.draw_aoe(hover_cell, "prev", Spells[self.battle.active_spell][ "prevision_aoe" ], "circle")
      else:
        self.grid.clean_prev()

      if clic and not self.clicking:
        self.clicking = True

        if hover_cell.area == "attack":
          if Spells[self.battle.active_spell]:
            if len(self.grid.prevision_aoe):
              target = []
              for cell in self.grid.prevision_aoe:
                target.append(cell)
            else:
              target = [hover_cell]
            Spells[self.battle.active_spell]["effect"](target)
            for cell in target:
              if cell.pion:
                if cell.pion.character.hp <= 0:
                  cell.pion.character = False
                  cell.pion = None
                
          self.battle.attacking = False
          self.ui.cancel_menu(self.battle)
          return
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
    if self.battle.change_turn == True:
      self.next_turn()
    if self.ui.clear_aoe:
      self.grid.clean_aoe()
      self.ui.clear_aoe = False
    if self.grid.active :
      if self.grid.active.pion:
        self.ui.set_character( self.grid.active.pion.character, self.battle, self.grid)
      else:
        self.grid.clean_active()

    else:
      self.ui.character = False
    pass

  def render(self, screen):
    screen.fill(colors.WHITE)
    self.grid.paint(screen)
    self.ui.draw(screen)
    self.ui.draw_buttons(screen)

    pass

  def next_turn(self):
    self.ui.set_turn(self.battle.turn)
    self.grid.clean_active()
    self.grid.clean_aoe()
    self.battle.change_turn = False
