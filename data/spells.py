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
      print(spell['name'] + " => " )
      target.pion.loose_pv(spell['damage'])
      print(f"{target.pion.character.name} - {spell['damage']} pv")

def add_token_to_all_targets(target, element, qte):
  for x in target:
    if x.pion:
      x.pion.character.add_tokens(element, qte)

def projection(grid, targets, origin, aoe, distance, type="from_origin", contact_effect=False):
  debug = False
  Targets= {"n":[], "s":[], "e":[], "w":[]}
  for target in targets:
    if target.pion and target.pion.position != origin:
      if target.pion.position[0] == origin[0]:
        if target.pion.position[1] - origin[1] < 0:
          Targets["n"].append(target)
        else:
          Targets["s"].append(target)
      if target.pion.position[1] == origin[1]:
        if target.pion.position[0] - origin[0] < 0:
          Targets["w"].append(target)
        else:
          Targets["e"].append(target)

  new_positions = []

  for direction in Targets:
    match direction:
      case "n":
        for target in Targets[direction]:
          new_position = (target.pion.position[0], max(target.pion.position[1] - distance, 0)) 
          if target.pion.position != ( new_position[0], new_position[1] ):
            destination = grid.get_cell( new_position[0], new_position[1] )
            grid.move(target, destination)
            new_positions.append(destination)
      case "w":
        for target in Targets[direction]:
          new_position = (max(target.pion.position[0] - distance, 0), target.pion.position[1]) 
          if target.pion.position!= ( new_position[0], new_position[1] ):
            destination = grid.get_cell( new_position[0], new_position[1] )
            grid.move(target, destination)
            new_positions.append(destination)
      case "s":
        for target in Targets[direction]:
          new_position = (target.pion.position[0], min(target.pion.position[1] + distance, grid.Y-1)) 
          if target.pion.position!= ( new_position[0], new_position[1] ):
            destination = grid.get_cell( new_position[0], new_position[1] )
            grid.move(target, destination)
            new_positions.append(destination)
      case "e":
        for target in Targets[direction]:
          new_position = (min(target.pion.position[0] + distance, grid.X-1), target.pion.position[1]) 
          if target.pion.position!= ( new_position[0], new_position[1] ):
            destination = grid.get_cell( new_position[0], new_position[1] )
            grid.move(target, destination)
            new_positions.append(destination)
            
  for target in new_positions:
    if target.pion and target.pion.position != origin:
      target.pion.detail()
        

# ====== [ Fireball ] ======
# Cost: 1N
# apply one fire token to the target
Fireball = Spell('Fireball', 8, "circle", 2)
def fireball_effect(target, grid): 
  direct_damage(Fireball, target)
  add_token_to_all_targets(target, 'fire', 1)
Fireball["effect"] = fireball_effect
Spells["Fireball"] = Fireball

# ====== [ Spark ] ======
# Cost: 1F 1PA
# all fire token of the target explode adding 2 dmg by token 
Spark = Spell('Spark', 3, "circle", 1, 2)
Spark_splinter = Spell('Splinter', 1, None, 2)
def spark_effect(target, grid): 
  direct_damage(Spark, target)
  for x in target:
    if x.pion:
      fire_token = x.pion.character.tokens['fire']
      for _ in range(fire_token):
        direct_damage(Spark_splinter, [x])
      fire_token = 0
  return 
Spark["effect"] = spark_effect
Spells["Spark"] = Spark

# ====== [ Splash ] ======
# push all targets 1m around to 3 m away
# apply one water token to targets
# apply status wet to targets
Splash = Spell('Splash', 0, "cross", 0, 1)
def splash_effect(target, grid):
  add_token_to_all_targets(target, 'water', 1)
  projection(grid, target, grid.active.pion.position, 0,3, "from", False)
Splash['effect'] = splash_effect
Spells['Splash'] = Splash

# ====== [ Frosw Wind ] ======

# ====== [ Water stream ] ======
Water_stream = Spell('Water stre.positionam', 4, "line", 3, 3)
def water_stream_effect(target, grid): direct_damage(Water_stream, target)
Water_stream["effect"] = water_stream_effect
Spells['Water stream'] = Water_stream
