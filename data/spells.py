Spells = {}

def Spell(name, reach, aoe, damage, prevision=False, prevision_type="circle"):
  return {
    'name': name,
    'range': reach,
    'aoe': aoe,
    'damage': damage,
    'prevision_aoe': prevision,
    'prevision_type': prevision_type,
    'effect': None
  }

def direct_damage(spell, targets):
  for target in targets:
    if target is not None and target.pion is not None:
      print(spell['name'] + " => " )
      target.pion.loose_pv(spell['damage'])
      print(f"{target.pion.character.name} - {spell['damage']} pv")

def add_token_to_all_targets(target, element, qte):
  for x in target:
    if x.pion:
      x.pion.character.add_tokens(element, qte)

def Collision(damage, targets): 
  spell = {"name":"collision", "damage": damage}
  direct_damage(spell, targets)

      
def projection(grid, targets, origin, distance, contact_effect=Collision):
  """
    Pushes targets on a grid away from an origin point in specific directions (N, S, E, W) by a specified distance.
    
    Args:
      grid: The game grid, providing methods for cell access and movement.
      targets: List of cells/entities to be evaluated.
      origin: (x, y) tuple representing the origin of the push effect.
      distance: Number of cells to push the targets.
      contact_effect: (Unused) Whether a contact effect is applied during the push.
    
    Returns:
      None
  """

  def calculate_new_position(direction, position):
    
    def detect_collision(grid, x,y, dx, dy, step):
      x_step, y_step = x + step * dx, y + step * dy
      obstacle_or_bound = grid.get_cell(x_step, y_step)

      x_in_bounds = -1 < x_step < grid.X
      y_in_bounds = -1 < y_step < grid.Y

      print(f"coord { (x_step, y_step) }")
      if not x_in_bounds or not y_in_bounds:
        print(f"out of bound {(x_step, y_step)}")
        print(f"daplacé à {(x_step -dx, y_step - dy)}")
        return  [obstacle_or_bound, (x_step - dx, y_step - dy)]
      
      has_obstacle = obstacle_or_bound.pion
      print(f"obstacle { obstacle_or_bound }")

      if has_obstacle:
        print(f"obstacle {(x_step, y_step)}")
        print(f"daplacé à {(x_step -dx, y_step - dy)}")
        return  [obstacle_or_bound, (x_step - dx, y_step - dy)]
      return False

    x, y = position
    
    match direction:
      case "n": dx, dy = 0, -1
      case "s": dx, dy = 0, 1
      case "e": dx, dy = 1, 0
      case "w": dx, dy = -1, 0

    collision_preview = False
    new_position = (x + dx * distance, y + dy * distance)
  
    for step in range(1, distance+1):
      collision_detected= detect_collision(grid, x, y, dx, dy, step)
      print(f"collision_detected {collision_detected}")
      if collision_detected:
        collision_preview = (abs((distance - step-1) * 3), collision_detected)
        new_position = collision_detected[1]
        return new_position, collision_preview
      
    return new_position, False
  
  Cardinals= {"n":[], "s":[], "e":[], "w":[]}
  
  for target in targets:
    if target.pion and target.pion.position != origin:
      x_diff = target.pion.position[0] - origin[0]
      y_diff = target.pion.position[1] - origin[1]
      
      if x_diff == 0: #same column
        if y_diff < 0: Cardinals["n"].append(target)
        else: Cardinals["s"].append(target)

      if y_diff == 0: #same row
        if x_diff < 0: Cardinals["w"].append(target)
        else: Cardinals["e"].append(target)

  Cardinals['n'].sort(key=lambda  x: x.pion.position[1])
  Cardinals['s'].sort(key=lambda  x: x.pion.position[1], reverse=True)
  Cardinals['w'].sort(key=lambda  x: x.pion.position[0])
  Cardinals['e'].sort(key=lambda  x: x.pion.position[0], reverse=True)

  for direction, targets in Cardinals.items():
    for target in targets:
      print("======")
      new_position, collision_preview = calculate_new_position(direction, target.pion.position)
      if target.pion.position != new_position:
        print(f"nouvelle position{new_position}")
        grid.move(target, grid.get_cell( *new_position ))
        if collision_preview:
          print(contact_effect)
          collision_preview[1][1] = grid.get_cell(*collision_preview[1][1])
          contact_effect(*collision_preview)

        


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
Splash = Spell('Splash', 3, "line", 0, 3, "line")
def splash_effect(target, grid):
  add_token_to_all_targets(target, 'water', 1)
  projection(grid, target, grid.hover, 3, Collision)
Splash['effect'] = splash_effect
Spells['Splash'] = Splash

# ====== [ Frosw Wind ] ======

# ====== [ Water stream ] ======
Water_stream = Spell('Water stream', 4, "line", 3, 3)
def water_stream_effect(target, grid):
  direct_damage(Water_stream, target)
Water_stream["effect"] = water_stream_effect
Spells['Water stream'] = Water_stream
