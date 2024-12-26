from data.mechanics import Mechanics
Spells = {}
    
class Spell:
  def __init__(self, name, reach, aoe, damage, prevision=False, prevision_type="circle"):
    self.name = name
    self.range = reach
    self.aoe = aoe
    self.damage = damage
    self.prevision_aoe = prevision
    self.prevision_type = prevision_type
    self.effect = None

  def define_effect(self, effect):
    self.effect = effect

  def cast(self, caster, targets, grid):
    print("================================================")
    print(f"Spell => {self.name}")
    if self.attempt_cast(caster) :
      self.effect(targets, grid)
    
  def __repr__(self):
    return (f"Spell(name={self.name}, range={self.range}, aoe={self.aoe}, "
      f"damage={self.damage}, prevision_aoe={self.prevision_aoe}, "
      f"prevision_type={self.prevision_type}, effect={self.effect})")

  def attempt_cast(self, caster):
    """
    Checks if the caster can pay the cost of a spell and deducts the cost if possible.
    
    Parameters:
        caster: The character object casting the spell, with resources like aura, tokens, hp, etc.
        
    Returns:
        True if the spell can be cast, False otherwise.
    """
    
    print(f"{caster.name} attempts to cast, {self.name}")

    success = True
    
    def check_spell_cost(ressource_name, ressource_pool, cost):
      check = True
      for element, required_value in cost.items():

        if element not in ressource_pool:
          print(f"Invalid ressource_pool '{element}' in {ressource_name}. Availible: {list(ressource_pool.keys())}")
          check = False
          continue

        if ressource_pool[element] < required_value:
          print(f"Not enough {element} in {ressource_name}: {required_value} needed, {ressource_pool[element]} availible")
          check = False
      return check

    def pay_cost(ressource_pool, cost):
      for element, required_value in cost.items():
        ressource_pool[element] -= required_value
    
    for stat, value in self.cost.items():
      match(stat):
        case "aura":
          if not check_spell_cost('aura', caster.aura, value):
            success = False
        case "tokens":
          if not check_spell_cost('tokens', caster.tokens, value):
            success = False
        case 'status':
          if next((status for status in caster.status if status.get('name') == value), None) is  None:
            print(f"{caster.name} must be under the status {value} to cast this spell")
            success = False
        case _:
          print(stat)
          if not stat in dir(caster):
            print(f"Invalid ressource_pool '{stat}'")
            success = False       
          elif getattr(caster, stat, 0) < value:
            print(f"Not enough {stat} : {value} needed, {getattr(caster, stat, 0)} availible")
            success = False       
          
    if success:
      for stat, value in self.cost.items():
        match(stat):
          case "aura":
            pay_cost(caster.aura, value)
          case "tokens":
            pay_cost(caster.tokens, value)
          case "status":
            next(status for status in caster.status if status['name'] == value)['level'] -= 1
          case _:
            setattr(caster, stat, getattr(caster, stat, 0) - value)
        
      print(f"{caster.name} successfully cast {self.name}")
      return True
    
    print(f"{caster.name} failed to cast {self.name}")
    return False

# ====== [ Fireball ] ======
# Cost: 1N
# apply one fire token to the target
Fireball = Spell('Fireball', 8, "circle", 2)
def fireball_effect(target, grid): 
  Mechanics[ "direct_damage" ]("Fireball", Fireball.damage, target)
  Mechanics[ "add_token_to_all_targets" ](target, 'fire', 1)
Fireball.define_effect( fireball_effect)
Fireball.cost = {"tokens": { "neutral": 2, "fire": 1}} 

# ====== [ Spark ] ======
# Cost: 1F 1PA
# all fire token of the target explode adding 2 dmg by token 
Spark = Spell('Spark', 3, "circle", 1, 2)
Spark_splinter = Spell('Splinter', 1, None, 2)
def spark_effect(target, grid): 
  Mechanics[ "direct_damage" ]("Spark", Spark.damage, target)
  for x in target:
    if x.pion:
      fire_token = x.pion.character.tokens['fire']
      for _ in range(fire_token):
        Mechanics[ "direct_damage" ]("Spark_splinter", Spark_splinter.damage, [x])
      fire_token = 0
  return 
Spark.define_effect( spark_effect )
Spark.cost = {"tokens": { "neutral": 1, "fire": 1}} 


# ====== [ Splash ] ======
# push all targets 1m around to 3 m away
# apply one water token to targets
# apply status wet to targets
Splash = Spell('Splash', 3, "line", 0, 3, "line")
def splash_effect(target, grid):
  Mechanics[ "add_token_to_all_targets" ](target, 'water', 1)
  Mechanics[ "projection" ](grid, target, grid.hover, 3, Mechanics[ "collision" ])
Splash.define_effect( splash_effect)
Splash.cost = {"tokens": {"neutral": 3}}

# ====== [ Frosw Wind ] ======

# ====== [ Stream ] ======
Stream = Spell('Stream', 4, "line", 3, 3)
def water_stream_effect(target, grid):
  Mechanics[ "direct_damage" ]("Stream", Stream.damage, target)
Stream.define_effect( water_stream_effect)
Stream.cost = {"mp": 2}

Spells["Fireball"] = Fireball
Spells["Spark"] = Spark

Spells['Stream'] = Stream
Spells['Splash'] = Splash
