from robot import *

r1 = robot()
r1.remove_edge((0,0),(0,1))
# print(r1.graph)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT :
            running = False 
 
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            
            if event.key == pg.K_SPACE:
                r1.explore()
            
            if event.key == pg.K_g:
                print(r1.graph  )

    draw_lab(window)
    r1.draw(window)
    r1.show_dist(window)


    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()
