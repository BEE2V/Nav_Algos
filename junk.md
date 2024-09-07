```python
import pygame as pg

import sys

pg.init()

C_W = 100
W_CELLS, H_CELLS = 6,4
GAP = 10

window = pg.display.set_mode((W_CELLS * (C_W + GAP) + GAP, H_CELLS * (C_W + GAP) + GAP))
pg.display.set_caption('Basic Pygame Loop')

clock = pg.time.Clock()

# wall ⏹, no wall ❎
h_walls = ["⏹⏹⏹⏹⏹⏹",
           "❎❎⏹⏹⏹❎",
           "❎❎❎⏹❎❎",
           "❎❎❎❎⏹❎",
           "⏹⏹⏹⏹⏹⏹"]

v_walls = ["⏹⏹❎❎❎❎⏹",
           "⏹⏹⏹❎❎❎⏹",
           "⏹❎⏹⏹⏹⏹⏹",
           "⏹⏹❎❎❎❎⏹"]

start = (0,3)
end = (4,2)

def draw_text(window, text, grid_coords: tuple):
    font = pg.font.SysFont(None, 24)
    text_surface = font.render(text, True, "#000000")
    text_rect = text_surface.get_rect()
    x = grid_coords[0] * (C_W + GAP) + GAP + (C_W - text_rect.width) // 2
    y = grid_coords[1] * (C_W + GAP) + GAP + (C_W - text_rect.height) // 2
    window.blit(text_surface, (x, y))           

def draw_rect(window, grid_cords:tuple, side_len, col):

    x = grid_cords[0]*(C_W + GAP) + GAP
    y = grid_cords[1]*(C_W + GAP) + GAP

    pg.draw.rect(window, col, (x,y,side_len,side_len))

def draw_labrynth(window, col="#d6edcc"):

    for j in range(H_CELLS + 1):
        for i in range(W_CELLS + 1):

            x = i*(GAP+C_W)
            y = j*(GAP+C_W)

            pg.draw.rect(window, "#000000", (x,y,GAP,GAP))

            draw_rect(window, (i,j), C_W, col)

    draw_text(window,"S",start)
    draw_text(window,"X",end)

def draw_walls(window, col="#000000"):
    for j, wall in enumerate(h_walls):
        for i, piece in enumerate(wall):
            if piece == "⏹":

                x = i*(GAP + C_W) + GAP
                y = j*(GAP + C_W)
                pg.draw.rect(window, col, (x, y, C_W, GAP)) 

    for j, wall in enumerate(v_walls):
        for i, piece in enumerate(wall):
            if piece == "⏹":

                x = i*(GAP + C_W)
                y = j*(GAP + C_W) + GAP
                pg.draw.rect(window, col, (x, y, GAP, C_W))                     



def draw_lab(window, cell_col='#d6edcc', wall_col='#000000', bg_col='#ffffff'):
    window.fill(bg_col)

    for j in range(2*H_CELLS + 1):
        for i in range(2*W_CELLS + 1):

            if i % 2 and j % 2:
                x = (i//2)*(C_W + GAP) + GAP
                y = (j//2)*(C_W + GAP) + GAP
                pg.draw.rect(window, cell_col, (x,y,C_W,C_W))

            elif i % 2 ^ j % 2:
                
            else:
                x = (i//2)*(C_W + GAP)
                y = (j//2)*(C_W + GAP)
                pg.draw.rect(window, wall_col, (x,y,GAP,GAP))




running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT :
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False


    # draw_labrynth(window)
    # draw_walls(window)

    draw_lab(window)


    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()


# optimize so that whole maze can be represented by one array
# pillars will be at even x even y
# walls will be at even x odd y  and odd x even y
# cells will be at odd x odd y

```

```python
# wall ⏹, no wall ❎
lab = ["⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹",
       "⏹❎❎❎❎❎❎❎❎❎❎❎⏹",
       "⏹❎⏹❎⏹❎⏹❎⏹❎⏹❎⏹",
       "⏹❎❎❎❎❎❎❎❎❎❎❎⏹",
       "⏹❎⏹❎⏹❎⏹❎⏹❎⏹❎⏹",
       "⏹❎❎❎❎❎❎❎❎❎❎❎⏹",
       "⏹❎⏹❎⏹❎⏹❎⏹❎⏹❎⏹",
       "⏹❎❎❎❎❎❎❎❎❎❎❎⏹",
       "⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹⏹"]

```

```python
lab = ["🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
       "🟦❎🟦❎❎❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦🟦🟦🟦🟦🟦🟦❎🟦",
       "🟦❎🟦❎🟦❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦❎🟦🟦🟦❎🟦❎🟦",
       "🟦❎❎❎🟦❎🟦❎🟦🟥🟦❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦🟦🟦❎🟦",
       "🟦🟨🟦❎❎❎❎❎❎❎❎❎🟦",
       "🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦"]
```

```python
def find_clusters(grid):
    def dfs(x, y):
        # If out of bounds or already visited or not an unexplored cell, return 0
        if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or visited[x][y] or grid[x][y] == 1:
            return 0
        # Mark the cell as visited
        visited[x][y] = True
        # Start with a cluster size of 1 (current cell)
        size = 1
        # Visit all 4 adjacent cells (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            size += dfs(x + dx, y + dy)
        return size

    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    clusters = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0 and not visited[i][j]:
                cluster_size = dfs(i, j)
                clusters.append((i, j, cluster_size))  # Store the starting cell and size of the cluster

    return clusters

# Example usage
grid = [
    [1, 0, 1, 1, 0],
    [1, 0, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [1, 0, 0, 1, 1],
    [1, 1, 1, 0, 0]
]

clusters = find_clusters(grid)
print(clusters)  # Output: list of clusters with their sizes

```