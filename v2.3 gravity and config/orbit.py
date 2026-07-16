from support.graphics import *

config=Config()
config.windowConfig.gdim = Vector2(1100,800)
config.gameConfig.do_ball_ball_collisions=False
config.gameConfig.g_coef=1000
config.windowConfig.ball_trail_list_len=10000

g=Game(config)

mainball=Ball(config.windowConfig.gdim/2,r=10,mass=1300,fixed=True)
g.world.add_ball(mainball)
# g.world.add_orbiter(mainball,mainball.r +30)
g.world.add_orbiter(mainball,mainball.r +70,ball_r=3,mass=10)
g.world.add_orbiter(mainball,mainball.r +200,ball_r=3,mass=10)
g.world.add_orbiter(mainball,mainball.r +300,ball_r=3,mass=10)
g.world.add_orbiter(mainball,mainball.r +120,ball_r=5,mass=10)
g.main_loop()