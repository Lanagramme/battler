*Améliorations de la mehode move*

pour le pion
move(origin, destination, grid)
  self.moves = moves - (abs(origin.x - destination.x) + abs(origin.y - destination.y) )
  grid.move(origin, destination)

pour la grid
move(orign, destination)
  pion = origin.pion

pour battle
if click and not self.clicking
  self.clicking = True
  if grid.hover.status == attack
    grid.active.pion.attack(current_attack, grid.hover.coord)
  elif grid.hover.pion 
    if gird.hover.status == move
      pass
    elif grid.hover.pion.team == turn.team
      activate(grid.hover.pion)
  else if grid.hover.status = move
    grid.hover.pion.move(grid.active.coord, grid.hover.coord)

penser a reset les moves du pion to move_max au turn
