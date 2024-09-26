import pygame as pg
import sys
from typing import Dict, List, Tuple

pg.init()

C_W = 100
W_CELLS, H_CELLS = 6,4
GAP = 10

window = pg.display.set_mode((W_CELLS * (C_W + GAP) + GAP, H_CELLS * (C_W + GAP) + GAP))
pg.display.set_caption('Basic Pygame Loop')

clock = pg.time.Clock()

# labyrinth designs
# wall 🟦, no wall ❎, start 🟨, end 🟥

"""
lab = ["🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
       "🟦❎❎❎❎❎❎❎❎❎❎❎🟦",
       "🟦❎🟦🟦🟦🟦🟦❎🟦🟦🟦🟦🟦",
       "🟦❎❎❎🟦❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦🟦🟦❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦🟥❎❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦❎🟦🟦🟦",
       "🟦🟨🟦❎❎❎🟦❎❎❎❎❎🟦",
       "🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦"]

lab = ["🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
       "🟦❎🟦❎❎❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦🟦🟦🟦🟦🟦🟦❎🟦",
       "🟦❎🟦❎🟦❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦❎🟦🟦🟦❎🟦❎🟦",
       "🟦❎❎❎🟦❎🟦❎🟦🟥🟦❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦🟦🟦❎🟦",
       "🟦🟨🟦❎❎❎❎❎❎❎❎❎🟦",
       "🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦"]
"""

lab = ["🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
       "🟦❎🟦❎❎❎❎❎❎❎❎❎🟦❎❎❎🟦",
       "🟦❎🟦❎🟦🟦🟦🟦🟦🟦🟦❎🟦🟦🟦❎🟦",
       "🟦❎🟦❎🟦❎❎❎❎❎❎❎❎❎🟦❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦🟦🟦🟦🟦❎🟦❎🟦",
       "🟦❎🟦❎❎❎🟦❎❎❎❎❎❎❎🟦❎🟦",
       "🟦❎🟦❎🟦🟦🟦❎🟦🟦🟦❎🟦🟦🟦❎🟦",
       "🟦❎❎❎❎❎🟦❎🟦❎❎❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦🟦🟦❎🟦🟦🟦🟦🟦❎🟦🟦🟦",
       "🟦❎🟦❎❎❎❎❎🟦❎❎❎❎❎🟦❎🟦",
       "🟦🟦🟦❎🟦❎🟦❎🟦❎🟦❎🟦🟦🟦❎🟦",
       "🟦❎🟦❎🟦❎🟦❎🟦❎🟦❎❎❎❎❎🟦",
       "🟦❎🟦❎🟦🟦🟦❎🟦❎🟦❎🟦🟦🟦❎🟦",
       "🟦❎❎❎❎❎❎❎🟦❎🟦❎🟦❎❎🟥🟦",
       "🟦❎🟦🟦🟦🟦🟦❎🟦❎🟦❎🟦❎🟦❎🟦",
       "🟦🟨❎❎❎❎❎❎❎❎🟦❎🟦❎❎❎🟦",
       "🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",]   

def draw_lab(window, cell_col='#d6edcc', wall_col='#919fb8', bg_col='#bce5f7'): # Draw the labyrinth
    """
    This method draws a labyrinth with the provided design
    """

    window.fill(bg_col)

    for j in range(2*H_CELLS + 1):
        for i in range(2*W_CELLS + 1):

            if i % 2 and j % 2:
                x = (i//2)*(C_W + GAP) + GAP
                y = (j//2)*(C_W + GAP) + GAP

                if   lab[j][i] == "🟨": col = "#e3750e"
                elif lab[j][i] == "🟥": col = "#eb2d5c"
                else                  : col = cell_col

                pg.draw.rect(window, col, (x, y, C_W, C_W)) # cells
                

            elif i % 2 and j % 2 == 0:
                if lab[j][i] == "🟦":
                    x = (i//2)*(GAP + C_W) + GAP
                    y = (j//2)*(GAP + C_W)
                    pg.draw.rect(window, wall_col, (x, y, C_W, GAP)) # horizontal walls                

            elif i % 2 == 0 and j % 2:
                if lab[j][i] == "🟦":
                    x = (i//2)*(GAP + C_W)
                    y = (j//2)*(GAP + C_W) + GAP
                    pg.draw.rect(window, wall_col, (x, y, GAP, C_W)) # vertical walls 

            else:
                x = (i//2)*(C_W + GAP)
                y = (j//2)*(C_W + GAP)
                pg.draw.rect(window, wall_col, (x, y, GAP, GAP)) # pillars

def draw_text(window, text, grid_coords: tuple): # Draw text
    """
    Draws text inside a given grid coordinates
    """
    font = pg.font.SysFont(None, 24)
    text_surface = font.render(str(text), True, "#000000")
    text_rect = text_surface.get_rect()
    x = grid_coords[0] * (C_W + GAP) + GAP + (C_W - text_rect.width) // 2
    y = grid_coords[1] * (C_W + GAP) + GAP + (C_W - text_rect.height) // 2
    window.blit(text_surface, (x, y))           

def evaluate()->tuple[dict[int, int], tuple[int, int], tuple[int, int]]:
    """
    Find start cell, end cell and Manhattan distance to end cell from each cell
    """
    # Search for the staring and ending grid coordinates
    for j in range(2*H_CELLS + 1):
        for i in range(2*W_CELLS + 1):

            if lab[j][i] == "🟨": start = (i//2,j//2)
            if lab[j][i] == "🟥": end = (i//2,j//2)

    # Calculate Manhattan distance from all the cells to the end cell
    dist = {}
    for j in range(H_CELLS):
        for i in range(W_CELLS):
            dist[(i,j)] = abs(i - end[0]) + abs(j - end[1])

    return dist, start, end