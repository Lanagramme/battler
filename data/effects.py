from data.mechanics import Mechanics
Status = {}

class Statut:
  def __init__(self, name, damage, type, cost, max_level  ):
    self.name = name            # Name of the status
    self.damage = damage        # Damage dealt (if applicable)
    self.cost = cost            # Cost to trigger the status (e.g., tokens in aura)
    self.type = type            # "withering" or other types
    self.max_level = max_level  # Maximum level for withering statuses
    self.effect = lambda target: None  # Default effect does nothing
    
  def cast(self, target):
    print("================================================")
    target_status = next((status for status in target.status if status['name'] == self.name), None)
    
    if self.attempt_trigger(target):
      if target_status is not None:
        match(self.type):
          case 'withering': target_status["level"] = self.max_level  
          case _: target_status["level"] += 1
      else:
        match(self.type):
          case 'withering': 
            target.status.append({"name":self.name, "level": self.max_level  })
          case _:
            target.status.append({"name":self.name, "level": 1})

      print(f"Statut => {self.name} Lv: {next(status['level'] for status in target.status if status['name'] == self.name)}")
      self.effect(target)
    else:
      print(f"Statut => {self.name} did not trigger")

  def define_effect(self, effect):
    self.effect = effect

  def life_cycle(self, target):
    """
    Handles the progression of the status on the target at the beginning of each turn.
    """
    target_status = next((status for status in target.status if status.get('name') == self.name), None)
    print("================================================")
    
    if not target_status:
      return

    trigger = self.attempt_trigger(target)
    
    match(self.type):
      case "growing":
        target_status["level"] += 1 if trigger else -1
      case 'withering':
        target_status["level"] = self.max_level if triggered else target_status["level"] - 1
      case 'static': 
        pass
      case _: 
        target_status["level"] -= 1

    if target_status['level'] == 0:
      print(f"Statut => {self.name} removed on {target.name}")
      target.status.remove(target_status)
    else:
      print(f"Statut => {self.name} Lv: {target_status['level']}")
      self.effect(target)
      
      
  
  def attempt_trigger(self, target):
    """
    Checks if the target is eligible for the status to trigger
    
    Parameters:
        target: The character object target by the spell, with ressources like aura, tokens, hp, etc.
        
    Returns:
        True if the status can be triggered, False otherwise.
    """
    
    print(f"{self.name} attempts to trigger on {target.name}")

    success = True
    
    def check_spell_cost(ressource_name, ressource_pool, cost):
      check = True
      available_keys = list(ressource_pool.keys())
      for element, required_value in cost.items():
        if element not in ressource_pool:
          print(f"Invalid ressource_pool '{element}' in {ressource_name}. Availible: {available_keys}")
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
          if not check_spell_cost('aura', target.aura, value):
            success = False
        case "tokens":
          if not check_spell_cost('tokens', target.tokens, value):
            success = False
        case 'status':
          if next((status for status in target.status if status.get('name') == value['name']), None) is  None:
            print(f"{target.name} must be under the status {value} to cast this spell")
            success = False
        case _:
          if not hasattr(target, stat):
            print(f"Invalid ressource '{stat}'")
            success = False       
          elif getattr(target, stat, 0) < value:
            print(f"Not enough {stat} : {value} needed, {getattr(target, stat, 0)} availible")
            success = False       
          
    if success:
      for stat, value in self.cost.items():
        match(stat):
          case "aura":
            pay_cost(target.aura, value)
          case "tokens":
            pay_cost(target.tokens, value)
          case "status":
            if value[ 'levels' ] == "A":
              target.status.remove(next(status for status in target.status if status['name'] == value['name']))
            else:
              next(status for status in target.status if status['name'] == value['name'])['level'] -= value
          case _:
            setattr(target, stat, getattr(caster, stat, 0) - value)
        
      print(f"{target.name} is now {self.name}")
      return True
    
    print(f"{self.name} did not trigger on {target.name}")
    return False


# ====== [ Burning ] ======
# Cost: 3aF
# direct damage equal to lv
Burning = Statut('Burning', 1, "static", {"aura":{"fire":3}}, 3)
def burning_effect(target):
  target_burning = next((status for status in target.status if status['name'] == "Burning"), None)
  if target_burning is not None:
    Mechanics['status_damage']("Burning", target_burning['level'], target)

Burning.define_effect(burning_effect)
    
  
Status['Burning'] = Burning

    
