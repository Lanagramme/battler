Mechanics = {}

class Effect():
  def cast():
    raise NotImplementedError("Effects must implement 'apply()'")

class Direct_damage(Effect):
  def __init__(self, damage):
    self.damage = damage

  def cast(self, target):
    if target and target.pion:
      target.pion.loose_pv(self.damage)
      print(f"{target.pion.character.name} -{self.damage} pv")

class Add_token(Effect):
  def __init__(self, element, qte):
    self.element = element
    self.qte = qte

  def cast(self, target):
    target.pion.character.add_tokens(self.element, self.qte)
    print(f"{target.pion.character.name} +{self.qte} {self.element}, tokens")

class Consume_token_and_hurt(Effect):
  def __init__(self, element, damage, multiplicator = 1):
    self.element = element
    self.damage = damage * multiplicator

  def cast(self, target):
    if target and target.pion:
      token = target.pion.character.tokens[self.element]
      for _ in range(token):
        target.pion.loose_pv(self.damage)
        print(f"{target.pion.character.name} -{self.damage} pv")
      target.pion.character.tokens[self.element] = 0


def status_damage(name, damage, target):
  target.hp -= damage
  print(f"{target.pion.character.name} -{damage} pv")

def add_token_to_all_targets(targets, element, qte):
  for x in targets:
    if x.pion:
      x.pion.character.add_tokens(element, qte)

def add_token(target, element, qte):
  target.pion.character.add_tokens(element, qte)

def repeat_for_token(target, element, effect):
  tokens = target.pion.character.token[element]
  if tokens: 
    for _ in range(tokens): 
      effect

def repeat_for_token_and_consume(target, element, effect):
  tokens = target.pion.character.token[element]
  if tokens: 
    for _ in range(tokens): effect
    target.pion.character.token[element] = 0

def collision(damage, targets): 
  direct_damage("collision", damage, targets)

def projection(grid, targets, origin, distance, contact_effect=collision):
  grid = self.grid
  targets = self.targets
  origin = self.origin
  distance = self.distance
  test = False
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

      if test: print(f"coord { (x_step, y_step) }")
      if not x_in_bounds or not y_in_bounds:
        if test: print(f"out of bound {(x_step, y_step)}")
        if test: print(f"daplacé à {(x_step -dx, y_step - dy)}")
        return  [obstacle_or_bound, (x_step - dx, y_step - dy)]
      
      has_obstacle = obstacle_or_bound.pion
      if test: print(f"obstacle { obstacle_or_bound }")

      if has_obstacle:
        if test: print(f"obstacle {(x_step, y_step)}")
        if test: print(f"daplacé à {(x_step -dx, y_step - dy)}")
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
      if test : print(f"collision_detected {collision_detected}")
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
      if test: print("======")
      new_position, collision_preview = calculate_new_position(direction, target.pion.position)
      if target.pion.position != new_position:
        if test: print(f"nouvelle position{new_position}")
        grid.move(target, grid.get_cell( *new_position ))
        if collision_preview:
          if test: print(contact_effect)
          collision_preview[1][1] = grid.get_cell(*collision_preview[1][1])
          contact_effect(*collision_preview)

class status:
  def __init__(self, name, cost, type, max, init, effect, cost_check= False, trigger = False):
    self.name = name
    self.cost = cost
    self.type = type
    self.max_level = max
    self.level = init
    self.effect = effect
    self.trigger = trigger
    
    self.pay_cost = cost_check

  def cast(self, target):
    if self.pay_cost(self.cost, target):
      target.status.append(self.name)    
      self.effect(target)
      return

  def apply_effect(self, target):
    if self.type == "wither" and pay_cost(self.cost):
      self.level = self.init
    elif self.type == "groth" and self.level < self.max_level and pay_cost(self.trigger):
      self.level = self.level + 1
    else:
      self.level = self.level - 1
      
    self.effect(self, target)
  
def frozen_effect(target):
  target.pm =0

Frozen = status('Frozen', {"aura":{"water":3}}, 'wither', 2, 2, frozen_effect)
# Frozen['pay_cost'] = default_cost

        

Mechanics[ "Consume_token_and_hurt" ] = Consume_token_and_hurt
Mechanics[ "Direct_damage" ] = Direct_damage
# Mechanics[ "direct_damage" ] = direct_damage
Mechanics[ "Add_token"     ] = Add_token
# Mechanics[ "add_token_to_all_targets" ] = add_token_to_all_targets
Mechanics[ "status_damage" ] = status_damage
Mechanics[ "collision" ] = collision
Mechanics[ "projection" ] = projection
