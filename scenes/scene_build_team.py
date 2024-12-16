import pygame
from classes.scene import Scene
from classes.ui import Button
from data.spells import Spells
from classes.character import Character
from utils.colors import colors
from utils.constants import WIDTH, HEIGHT

spells = [Spells["Fireball"], Spells['Stream']]
spells2 = [Spells["Splash"], Spells['Spark']]
characters = []
team = []
buttons = []
spots = []

Touko = Character('Touko',  2, 4, 4, './sprite_sheet/past.png'  , spells, ["bottom", "left", "right", "top"], 60, 60)
Girl  = Character('Girl' ,  2, 4, 3, './sprite_sheet/girl.png'  , spells, ["bottom", "left", "right", "top"], 60, 60, -3)
Scott = Character('Scott', 12, 4, 5, './sprite_sheet/Scott.png' , spells, ["bottom", "left", "right", "top"], 60, 60, -6)
Green = Character('Green', 12, 4, 5, './sprite_sheet/green.png' , spells, ["bottom", "left", "right", "top"], 60, 60, -6)
Azure = Character('Azure', 12, 4, 3, './sprite_sheet/azure.png' , spells, ["bottom", "left", "right", "top"], 60, 60, -6)
Lance = Character('Lance', 12, 4, 5, './sprite_sheet/silver.png', spells2, ["bottom", "left", "right", "top"], 60, 60, -6)
Demo  = Character('Demo' , 12, 4, 3, './sprite_sheet/Demo_sprite2.png', spells, ["bottom", "left", "right", "top"], 34, 40, 5)
Professor = Character('Professor', 12, 4, 5, './sprite_sheet/professor.png', spells, ["bottom", "left", "right", "top"], 60, 60)

characters = [Lance,  Azure, Girl, Demo,  Green,  Scott]

class TeamSelect(Scene):
  def __init__(self, state):
    super().__init__()
    self.font = pygame.font.Font(None, 40)
    self.next = False
    self.btn_next = Button(
      WIDTH - 150, HEIGHT - 150, 130, 50, "Battle !!!", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36,
      action=self.battle
    )
    self.state = state

    for i, character in enumerate(characters):
      x = (i+1) * 100
      btn = Button(
        x, 100, 50, 50, "", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36,
        action=lambda ch=character: self.add_to_team(ch)
      )
      buttons.append(btn)

  def handle_events(self, events):
    if self.next:
      return 'battle'
    for event in events:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          return 'menu'

      for button in buttons:
        button.handle_event(event)

      for button in spots:
        button.handle_event(event)

      self.btn_next.handle_event(event)
        
  def update(self):
    pass
    
  def render(self, screen):
    
    screen.fill((30, 30, 30))  # Dark background
    title = self.font.render('Chose three members for your team', True, (255, 255, 255))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(title, title_rect)


    for i, (character, button) in enumerate(zip(team, spots)):
      button.draw(screen)
    
      sprite = character.sprite["bottom"][0]
      sprite_rect = sprite.get_rect()
      sprite_center_x = button.rect.x + (button.rect.width - sprite_rect.width) // 2
      sprite_center_y = button.rect.y + (button.rect.height - sprite_rect.height) // 2 + character.offsetx

      screen.blit(sprite, (sprite_center_x, sprite_center_y))
      
    for i, (character, button) in enumerate(zip(characters, buttons)):
      button.draw(screen)

      sprite = character.sprite["bottom"][0]
      sprite_rect = sprite.get_rect()
      sprite_center_x = button.rect.x + (button.rect.width - sprite_rect.width) // 2
      sprite_center_y = button.rect.y + (button.rect.height - sprite_rect.height) // 2 + character.offsetx

      screen.blit(sprite, (sprite_center_x, sprite_center_y))

    if len(team) == 3:
      self.btn_next.draw(screen)
      
  def add_to_team(self, character):
    global spots
    if len(team) < 3 and character not in team:
      team.append(character)
    self.set_spots()
      

  def set_spots(self,):
    global spots
    spots = []
    for i, member in enumerate(team):
      x = 250 + (i*100)
      btn = Button(
        x, 300, 50, 50, "", colors.BLUE, colors.DARK_BLUE, colors.BLACK, 36,
        action=lambda ch=member: self.rem_from_team(ch)
      )
      spots.append(btn)

  def rem_from_team(self, character):
    if character in team:
      team.remove(character)
    self.set_spots()
      
  def battle(self):
    self.next = True
    self.state.setup(team)
    
