Spells = {}

def Spell(name, reach, aoe, damage, prevision=False):
  return {
    'name': name,
    'range': reach,
    'aoe': aoe,
    'damage': damage,
    'prevision_aoe': prevision,
    'effect': None
  }

def direct_damage(spell, targets):
  for target in targets:
    if target.pion is not None:
      target.pion.loose_pv(spell['damage'])

# def get_spell_targets(spell):
#   targets = []
#   for cell in grid.attack_aoe:
#     if cell.pion is not False:
#       targets.append(cell)
#   return targets

# ====== [ Fireball ] ======
Fireball = Spell('Fireball', 8, "circle", 3, 1)
def fireball_effect(target): direct_damage(Fireball, target)
Fireball["effect"] = fireball_effect
Spells["Fireball"] = Fireball

# ====== [ Water stream ] ======

Water_stream = Spell('Water stream', 4, "line", 3, 3)
def water_stream_effect(target): direct_damage(Water_stream, target)
Water_stream["effect"] = water_stream_effect
Spells['Water stream'] = Water_stream

# ====== [ Spark ] ======
# Cost: 1F 1PA
# all fire token of the target explode adding 2 dmg by token 
Spark = Spell('Spark', 3, "circle", 2, 0)
def spark_effect(target): 
  direct_damage(Spark, target)
Spark["effect"] = spark_effect
Spells["Spark"] = Spark
