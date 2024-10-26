# Documentation for battles

## Classes

[Pion](#Pion)
[Cell](#Cell)
[Grid](#Grid)

#### Pion 
  Create a pion.
  @param {string} team
  @param {coord} position
  
  @prop {string} team
  @prop {coord} position


#### Cell 
  Cell of the grid
  @param {number} x
  @param {number} y
  @param {number} margin - distance between the window border and the grid
  @param {number} gutter - space between the cell and it's neibourghs
  @param {number} size
  @param {bool} hover - is the mouse hovering the cell
  @param {bool} active
  @param {bool /number} pion - either false of the pion's index in LIST_PIONS
  
  @prop {number} x
  @prop {number} y
  @prop {number} padding - distance between the cell's border and the pion's (5)
  @prop {coord} dimensions - (@param size, @param size)
  @prop {bool} hover
  @prop {bool} active
  @prop {string} color
  @prop {bool /number} pion - either false of the pion's index in LIST_PIONS
  @param {PyGame object} body
  
  
  @method def_color 
    define the color of the cell depending of if it is hovered, active or neutral
    
  @method draw
    draw the cell on the board
    draw the pion it contains if any
    @param {PyGame object} SCREEN
    @param {bool} has_pion
    @param {string} pion_color

#### Grid
  Main state machine of the game
  @param {number} width - width of a cell
  @param {number} height - height of a cell
  @param {number} margin - distance between the window border and the grid
  @param {number} gutter - space between the cell and it's neibourghs
  @param {number} size - size of a cell
  
  @prop {number} margin - distance between the window's border and the grid
  @prop {number} gutter - space between cells
  @prop {number} size - size of a cell
  @prop {number} width - width of a cell
  @prop {number} height - height of a cell
  @prop {number} spanX - width of the board
  @prop {number} spanY - height of the board
  @prop {array} cells
  @prop {bool} hover
  @prop {coord} active - (None, None)
  
  @method activate
    define the @prop active
    @param {number} x
    @param {number} y
    
  @method reset
    set the value of all the cells in @prop cells to False
    
  @method paint
    draw the grid on the screen
    @param {PyGame object} SCREEN
