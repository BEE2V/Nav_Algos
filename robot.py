from labyrinth import *

class robot:
    def __init__(self) -> None:
        self.explored = [["⬛" for i in range(W_CELLS)] for j in range(H_CELLS)] # ⬛- not explored, ⬜- explored
        self.estm_dist, self.start , self.target = evaluate() # Identify these by scanning the labyrinth
        self.pos = self.start
        self.came_from, self.going_to = [None]*2
        self.journey = {} # Jouney taken by the robot

        self.graph: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}   # To store all edges between cells
        self.generate_graphs() # Graph of neighbours
        # Store all removed edges between cells (Walls)
        self.seen_labyrinth = [
            [cell if (i == 0 or i == len(lab) - 1 or j == 0 or j == len(row) - 1) else "🟩"
            for j, cell in enumerate(row)]
            for i, row in enumerate(lab)
        ]

        self.exploring = True # True - Exploring, False - Returning


        # self.pos = (5, 2)

    def get_neighbours(self, cell_cords, lab_cords):
        '''
        returns a dictionary for all 4 neighbouring cells with data {"direction":(a,b)}
         - a = estimated distances from the cell to the end cell, if theres a cell ,unless the cell is blocked by a wall
         - b = whether the cell already is explored "⬜" or not "⬛"
        '''
        
        i, j = cell_cords
        x, y = lab_cords

        up, down, right, left = [("blocked", "⬜") for i in range(4)]

        if i == 0: left = ("no_cell", "⬜")              # handling corners
        if i == W_CELLS -1: right = ("no_cell", "⬜")
        if j == 0: up = ("no_cell", "⬜")
        if j == H_CELLS - 1: down = ("no_cell", "⬜")

        # if the choosen cell is not blocked by a wall "❎", save the distance and if it's explored to the dict
        if up[0]     == "blocked" and lab[y-1][x] == "❎": up    = (self.estm_dist[(i, j-1)] , self.explored[j-1][i])   
        if down[0]   == "blocked" and lab[y+1][x] == "❎": down  = (self.estm_dist[(i, j+1)] , self.explored[j+1][i])
        if left[0]   == "blocked" and lab[y][x-1] == "❎": left  = (self.estm_dist[(i-1, j)] , self.explored[j][i-1])
        if right[0]  == "blocked" and lab[y][x+1] == "❎": right = (self.estm_dist[(i+1, j)] , self.explored[j][i+1])

        neighbours = {"up":up, "right":right, "down":down, "left":left}

        return neighbours

    def explore(self):
        '''
        explore through the labyrinth while doing the following
        \n1. check for walls between current cell and neighbour cells
        \n2. if there's a wall, remove the connections(edges) between those cells
        \n3. select a cell to travel in the next step
        \n4. update the distances to each cell from the target cell
        \n5. update the self.journey
        '''

        self.came_from = self.pos
        
        if self.going_to != None: self.pos = self.going_to

        i, j = self.pos
        x, y = 2*i + 1, 2*j + 1

        neighbours = self.get_neighbours((i,j),(x,y))
        # dir = min(neighbours, key=neighbours.get)

        selected = [100000, "⬛", "up"]
        for neighbour in neighbours: # choosing next cell
            val, visited = neighbours[neighbour]

            if val == "no_cell": continue
            if val == "blocked":    # If the neighbour is blocked by a wall, remove the edge(connection) between current cell and that cell in the graph
                nav = {"up":(0,-1), "right":(1,0), "down":(0,1), "left":(-1,0)}
                dx, dy = nav[neighbour]
                self.remove_edge(self.pos, (i+dx, j+dy))

            if selected[1] == visited and selected[0] > val: selected = [val, visited, neighbour] # If neighbour is already visited but "selected" is not updated with a better cell, choose this even though it's already visited
            if selected[1] == "⬜" and visited == "⬛": selected = [val, visited, neighbour] # If the selected cell is a visited one, but current is not, update "selected" with current cell

        if selected == [100000, "⬛", "up"]: # 180 rotations, if "selected" hasn't changed meaning no better cell has found
            selected = self.journey[self.came_from]

            invert = {"up":"down", "right":"left", "down":"up", "left":"right"}

            selected[-1] = invert[selected[-1]]

        # If robot has come to the target, calculate the optimal path from staring square
        if self.pos == self.target:
            
            self.optimal_path:list[tuple[int,int]] = [self.start]
            dist, cords = 100000, self.start

            while cords != self.target:
                cells = self.graph[cords]

                for cell_cords in cells:
                    if self.estm_dist[cell_cords] < dist:
                        dist = self.estm_dist[cell_cords]
                        cords = cell_cords
                self.optimal_path.append(cords)  

            self.exploring = False      


        self.journey[self.pos] = selected # Update the self.journey with the selected cell
        self.update_vals(self.target, self.graph) # Update the distance values to the target cell from all other cells according to newly found walls


        dir = selected[-1]  # Update the robot traveling direction and next going cell

        if dir == "up"   : self.going_to = (i, j - 1)
        if dir == "right": self.going_to = (i + 1, j)
        if dir == "down" : self.going_to = (i, j + 1)
        if dir == "left" : self.going_to = (i - 1, j)

        self.explored[j][i] = "⬜" # mark self.pos as visited

        # print(f"came={self.came_from} pos={self.pos}\t dir={dir}\t going={self.going_to}")

    def go_optimaly(self,from_start = False):
        '''
        robot travels in the optimal path from start or from target as defined
        '''
        if self.optimal_path:
            i = 0 if from_start else -1
            self.pos = self.optimal_path.pop(i)
        else:
            print('Reached the target through optimal path')

        

    def draw(self, window, col="#1df24f"):
        '''
        draw the robot in its position on the labyrinth
        '''
        i, j = self.pos
        x = i*(C_W + GAP) + GAP
        y = j*(C_W + GAP) + GAP
        pg.draw.rect(window, col, (x, y, C_W, C_W))
        
    def draw_seen_labyrinth(self, window, wall_col='#024461'):
        '''
        draw the walls seen and stored in robot's memory
        '''

        for j in range(2*H_CELLS + 1):
            for i in range(2*W_CELLS + 1):                    
                
                if i % 2 and j % 2 == 0:
                    if self.seen_labyrinth[j][i] == "🟦":
                        x = (i//2)*(GAP + C_W) + GAP
                        y = (j//2)*(GAP + C_W)
                        pg.draw.rect(window, wall_col, (x, y, C_W, GAP)) # horizontal walls                

                elif i % 2 == 0 and j % 2:
                    if self.seen_labyrinth[j][i] == "🟦":
                        x = (i//2)*(GAP + C_W)
                        y = (j//2)*(GAP + C_W) + GAP
                        pg.draw.rect(window, wall_col, (x, y, GAP, C_W)) # vertical walls

                elif not(i % 2 and j % 2):
                    if self.seen_labyrinth[j][i] == "🟦":
                        x = (i//2)*(C_W + GAP)
                        y = (j//2)*(C_W + GAP)
                        pg.draw.rect(window, wall_col, (x, y, GAP, GAP)) # pillars       
    
    def generate_graphs(self):
        '''
        Generate a dictionary, where all the neighbours for a given cell is stored. 
        \n(record same connection twice {a:'b',  b:'a'})
        '''
        
        for j in range(H_CELLS):
            for i in range(W_CELLS):
                
                neighbours = []
                for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                    x, y = i + dx, j + dy

                    if x < 0 or x >= W_CELLS or y < 0 or y >= H_CELLS:
                        continue
                    neighbours.append((x,y))
                        
                self.graph[(i,j)] = neighbours

    def remove_edge(self,cord_1,cord_2):
        '''
        remove the two edges between given cells in the graph 
        \nboth {a:'b', b:'a'}
        '''

        if cord_2 in self.graph[cord_1]:
            self.graph[cord_1].remove(cord_2) 

        if cord_1 in self.graph[cord_2]:
            self.graph[cord_2].remove(cord_1)  
        
        self.update_seen_lab(cord_1, cord_2)

    def update_seen_lab(self, cord_1, cord_2):
        '''
        when removing an edge(robot has seen a wall),
        \nthis method will mark a wall in robots memory
        '''

        n1, m1 = cord_1
        n2, m2 = cord_2

        x = 2*n1 + 1 + (n2 - n1) 
        y = 2*m1 + 1 + (m2 - m1)

        if m1 == m2:
            self.seen_labyrinth[y-1][x] = '🟦'
            self.seen_labyrinth[y  ][x] = '🟦'
            self.seen_labyrinth[y+1][x] = '🟦'
        if n1 == n2:
            self.seen_labyrinth[y][x-1] = '🟦'
            self.seen_labyrinth[y][x  ] = '🟦'
            self.seen_labyrinth[y][x+1] = '🟦'

    def update_vals(self, pos, graph):
        '''
        update the distance to all cells from the target cell, 
        \nthrough the edges(connections) defined in graph/(self.graph)
        '''

        visited = []
        queue = []

        visited.append(pos)
        queue.append(pos)
        self.estm_dist[pos] = 0

        while queue:
            c = queue.pop(0)
            
            for cord in graph[c]:
                if cord not in visited:
                    visited.append(cord)
                    queue.append(cord)
                    self.estm_dist[cord] = self.estm_dist[c] + 1

    def show_dist(self, window):
        '''
        display the calculated distances on the cells of the labyrinth
        '''
        for cell in self.estm_dist:
            draw_text(window, self.estm_dist[cell], cell)