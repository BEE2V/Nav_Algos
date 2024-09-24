from robot import *

r1 = robot()

running = True
while running:                              # Main loop
    for event in pg.event.get():
        if event.type == pg.QUIT :          # Quitting
            running = False 
 
        elif event.type == pg.KEYDOWN:      # Quitting
            if event.key == pg.K_ESCAPE:
                running = False
            
            if event.key == pg.K_SPACE:     # Exploring
                if r1.exploring:
                    r1.explore()
                else:
                    r1.go_optimaly()
            
            if event.key == pg.K_g:         # Showing graph   
                print(r1.graph  )

    draw_lab(window)                        # Drawing labrynth
    r1.draw(window)                         # Drawing Robot
    r1.draw_seen_labrynth(window)           # Drawing the walls seen by the robot
    r1.show_dist(window)                    # Displaying distances


    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()
