from support.graphics import *

dim=(600,600)
g=Game(dim)

# make walls
g.world.edge_walls()

r=1
pad=10

sh=r+pad
s=sh*2

for ix in range(dim[0]//s):
    for iy in range(dim[1]//s):
        x=(ix+.5)*s
        y=(iy+.5)*s
        c=g.world_to_screen_v(Vector2(x,y))
        g.world.add_ball(Ball(c,r=r))
        # print(x,y)
        
g.main_loop()