class Mouse:
    def __init__(self) -> None:
        '''
        Initialize variables to keep track of the labyrinth
        ##### labyrinth Data
        \nIf the labyrinth is MxN rows x columns
        \nlabyrinth matrix will be of size (2M + 1) x (2N +1)
        \n(x, y) - wall/cells
        - (Odd, Odd) - Cell
        - (Even, Odd) - Walls horizontal
        - (Odd, Even) - Walls vertical
        - (Even, Even) - Posts
        - Store cell data like the flooded value for cell, in cell coordinates
        - Store wall data, in wall coordinates
            - 00 - No wall
            - 01 - Physical Wall
            - 10 - Not Scanned
            - 11 - Virtual Wall
        - Nothing will be stored in post locations
        ##### Mouse Position
        ##### Mouse Facing Direction
        - Use NESW to store the mouse absolute rotation    
        '''
        
    def move(self, distance) -> None:
        '''
        Move forward a given distance
        \nCell width should be defined
        '''
        
    def turn(self,angle) -> None:
        '''
        Rotate by a given angle
        \n(-180...-90...0...90...180)
        '''
    
    def sense_walls(self) -> None:
        '''
        Activate sensors to see if there are any walls in
        - Left
        - Front
        - Right
        '''
        
    def update_map(self, position:tuple[int, int], LFR:int) -> None:
        '''
        Update the labyrinth matrix depending on following attributes
        - Position
        - Absoulte rotaion
        - Wall data
            - Wall data will be provided in a 3 bit binary number
            - 0 indicates no wall
            - 1 indicates wall
            - 000 -> provides wall data in order Left, Front, Right of robots relative direction
            - Should identify the real direction of those walls before updating
        '''
        
    def explore_in(self) -> None:
        '''
        Mouse explores in towards the labyrinth center while floding the labyrinth matrix
        '''
        
    def expore_out(self) -> None:
        '''
        Mouse explores out towards the corner of the labyrinth maximizing the searched area
        - Mouse will go towards largest cluster of unexplored area
            One way of doing that is ; 
            - When the mouse is at the center, divide the labyrinth into 4 or more sections (Small squares)
            - Identify the most unexplored sector
            - Rote the return path such that those areas will be explored
        '''
        
    def draw(self) -> None:
        '''
        Draw the mouse in its current position
        '''