from support.graphics import *

config=Config()

config.windowConfig.gdim = Vector2(1100,800)
config.gameConfig.do_ball_ball_collisions=True
config.gameConfig.g_coef=-100
config.gameConfig.max_ball_size=10

g=Game(config)

# make walls
g.world.edge_walls()
# g.world.walls+=[Wall(Vector2(0,0),Vector2(500,500)),Wall(Vector2(500,0),Vector2(0,500))]

# g.world.add_ball(Ball((50,10),(0,-101),r=10))
# g.world.add_ball(Ball((240,10),(0,-110),r=5))
# g.world.add_ball(Ball((50,140),(0,-110),r=20))

g.main_loop()