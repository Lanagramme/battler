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

class Collision(Effect):
  def __init__(self):
    self.effects = []
    self.grid_effects = []

  def add_effect(self, effect):
    self.effects.append(effect)

  def add_grid_effect(self, effect):
    self.grid_effects.append(effect)

  def cast(self, target):
    if target:
      print(f"{target.pion.character.name} collided!")
      for effect in self.effects:
          effect.cast(target)

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

class Projection(Effect):
  def __init__(self, distance):
    self.contact_effect = Collision()
    self.distance = distance

  def add_collision_effect(self, effect):
    self.contact_effect.add_effect(effect)

  def cast(self, caster, targets, grid):
    test = False
    origin = grid.hover
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
      def detect_collision(x,y, dx, dy, step):
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
      new_position = (x + dx * self.distance, y + dy * self.distance)
    
      for step in range(1, self.distance+1):
        collision_detected= detect_collision(x, y, dx, dy, step)
        if test : print(f"collision_detected {collision_detected}")
        if collision_detected:
          collision_preview = (abs((self.distance - step-1) * 3), collision_detected)
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
            if test: print(self.contact_effect)
            # collision_preview[1][1] = grid.get_cell(*collision_preview[1][1])
            print(collision_preview)
            # self.contact_effect.cast(*collision_preview)
            self.contact_effect.cast(grid.get_cell(*collision_preview[1][1]))

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

Mechanics[ "Consume_token_and_hurt" ] = Consume_token_and_hurt
Mechanics[ "Direct_damage" ] = Direct_damage
Mechanics[ "Add_token"     ] = Add_token
# Mechanics[ "status_damage" ] = status_damage
Mechanics[ "Collision" ] = Collision
Mechanics[ "Projection" ] = Projection
