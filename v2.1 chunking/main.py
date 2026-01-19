from support.graphics import *
g=Game((600,600),3)

# make walls
g.world.edge_walls()
# g.world.walls+=[Wall(Vector2(0,0),Vector2(500,500)),Wall(Vector2(500,0),Vector2(0,500))]

# g.world.add_ball(Ball((50,10),(0,-101),r=10))
# g.world.add_ball(Ball((240,10),(0,-110),r=5))
# g.world.add_ball(Ball((50,140),(0,-110),r=20))

g.main_loop()