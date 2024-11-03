Spells = {}

def Spell(name, reach, aoe, damage, prevision=False):
  return {
    'name': name, "range":reach, 'aoe': aoe, 'damage': damage, "prevision_aoe": prevision
  }

def direct_damage(spell, targets):
  for target in targets:
    if target.pion is not None:
      target.pion.loose_pv(spell['damage'])

def get_spell_targets(spell):
  targets
  for cell in grid.attack_aoe:
    if cell.pion is not False:
      targets.append(cell)
  return targets

Spells["Fireball"] = Spell('Fireball', 8, "circle", 3, 1)

def fireball_effect(target):
  spell = Spells['Fireball']
  direct_damage(Spells['Fireball'], target)

Spells['Fireball']["effect"] = fireball_effect

Spells['Water stream'] = Spell('Water stream', 4, "line", 3, 3)
 
def water_stream_effect(target):
  spell = Spells['Water stream']
  direct_damage(spell, target)

Spells['Water stream']["effect"] = water_stream_effect

