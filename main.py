from robot import *

r1 = robot()
r1.remove_edge((0,0),(0,1))
# print(r1.graph)

running = True
while running:                              # Main loop
    for event in pg.event.get():
        if event.type == pg.QUIT :          # Quitting
            running = False 
 
        elif event.type == pg.KEYDOWN:      # Quitting
            if event.key == pg.K_ESCAPE:
                running = False
            
            if event.key == pg.K_SPACE:     # Exploring
                r1.explore()
            
            if event.key == pg.K_g:         # Showing graph   
                print(r1.graph  )

    draw_lab(window)                        # Drawing labrynth
    r1.draw(window)                         # Drawing Robot
    # r1.draw_seen_walls(window)              # Drawing the walls seen by the robot
    r1.show_dist(window)                    # Displaying distances


    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()
