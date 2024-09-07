from maze import *

class robot:
    def __init__(self) -> None:
        self.explored = [["⬛" for i in range(W_CELLS)] for j in range(H_CELLS)]
        self.estm_dist, self.pos , self.target = evaluate()
        self.came_from, self.going_to = [None]*2
        self.journey = {}

        self.graph = {}
        self.generate_graph()

        # self.pos = (5, 2)

    def get_neighbours(self, cell_cords, lab_cords):
        i, j = cell_cords
        x, y = lab_cords

        up, down, right, left = [("blocked", "⬜") for i in range(4)]

        if i == 0: left = ("no_cell", "⬜")
        if i == W_CELLS -1: right = ("no_cell", "⬜")
        if j == 0: up = ("no_cell", "⬜")
        if j == H_CELLS - 1: down = ("no_cell", "⬜")

        if up[0]     == "blocked" and lab[y-1][x] == "❎": up    = (self.estm_dist[(i, j-1)] , self.explored[j-1][i])
        if down[0]   == "blocked" and lab[y+1][x] == "❎": down  = (self.estm_dist[(i, j+1)] , self.explored[j+1][i])
        if left[0]   == "blocked" and lab[y][x-1] == "❎": left  = (self.estm_dist[(i-1, j)] , self.explored[j][i-1])
        if right[0]  == "blocked" and lab[y][x+1] == "❎": right = (self.estm_dist[(i+1, j)] , self.explored[j][i+1])

        neighbours = {"up":up, "right":right, "down":down, "left":left}

        return neighbours

    def explore(self):

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
            if val == "blocked": 
                nav = {"up":(0,-1), "right":(1,0), "down":(0,1), "left":(-1,0)}
                dx, dy = nav[neighbour]
                self.remove_edge(self.pos, (i+dx, j+dy))

            if selected[1] == visited and selected[0] > val: selected = [val, visited, neighbour] 
            if selected[1] == "⬜" and visited == "⬛": selected = [val, visited, neighbour]

        if selected == [100000, "⬛", "up"]: # 180 rotations
            selected = self.journey[self.came_from]

            invert = {"up":"down", "right":"left", "down":"up", "left":"right"}

            selected[-1] = invert[selected[-1]]

        self.journey[self.pos] = selected

        self.update_vals(self.target, self.graph)


        dir = selected[-1]

        if dir == "up"   : self.going_to = (i, j - 1)
        if dir == "right": self.going_to = (i + 1, j)
        if dir == "down" : self.going_to = (i, j + 1)
        if dir == "left" : self.going_to = (i - 1, j)

        self.explored[j][i] = "⬜"

        # print(f"came={self.came_from} pos={self.pos}\t dir={dir}\t going={self.going_to}")

    def draw(self, window, col="#1df24f"):
        i, j = self.pos
        x = i*(C_W + GAP) + GAP
        y = j*(C_W + GAP) + GAP
        pg.draw.rect(window, col, (x, y, C_W, C_W))
        
    def generate_graph(self):
        
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

        if cord_2 in self.graph[cord_1]:
            self.graph[cord_1].remove(cord_2)  

        if cord_1 in self.graph[cord_2]:
            self.graph[cord_2].remove(cord_1)  

    def update_vals(self, pos, graph):
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

        for cell in self.estm_dist:
            draw_text(window, self.estm_dist[cell], cell)