from .dataclasses import *



def sign(v):
    if v >0:
        return 1
    if v<0:
        return-1
    if v==0:
        return 0

def in_range(v,min,max):
    """inrange inclusive"""
    if v >= min and v <= max:
        return True
    return False

class Ball:
    def __init__(self,p,v=(0,0),a=(0,0),r=3,bounce_factor=.8,fixed=False):
        self.pos=Vector2.to_V2(p)
        self.v=Vector2.to_V2(v)
        self.a=Vector2.to_V2(a)
        self.r=r
        self.fixed=fixed
        self.bounce_factor=bounce_factor
    
    def copy(self):
        return Ball(self.pos,self.v,self.a,self.r)
    
    def __str__(self):
        return f"Ball({self.pos},{self.v})"

class Wall:
    def __init__(self,p1:Vector2,p2:Vector2,bounce_factor=0.8):
        self.p1=p1
        self.p2=p2
        

        self.lengh=(p1-p2).magnitude()

        # direction vectr
        # P1 -> P2
        self.v_dir=p2-p1
        # normal vector
        self.v_norm=Vector2(self.v_dir.y,-self.v_dir.x)

        self.bounce_factor=bounce_factor

        # print(self.v_dir*self.v_norm)

    def dist_from_wall(self,p):
        """signed"""
        p=Vector2.to_V2(p)
        v=p-self.p1
        d=v.scalar_res(self.v_norm)
        return d
    

    def __str__(self):
        return f"Wall({str(self.p1)} to {str(self.p2)})"
    



# class Physics:

# def do_ball_wall_collision(wall:Wall,ball:Ball):
#     d_n=wall.dist_from_wall(ball.pos)
    
#     if d_n > ball.r:
#         return False
    
#     # wall p1 to ball
#     v=ball.pos-wall.p1

#     # - <- P1 0 -> P2 +
#     d_along_wall = v.scalar_res(wall.v_dir)

#     # mid type
#     if in_range(d_along_wall,0,wall.lengh):
#         # reflect velocity vector perpendicular to wall
#         v_n=ball.v.v_res(wall.v_norm)
#         ball.v -= (v_n*2)


class Physics:
    def __init__(self,world):
        self.world=world
    
    def p_contact_ball_wall(ball:Ball,wall:Wall):
        pass

    def reflect_v(self,v:Vector2,d:Vector2,ratio=1):
        if d.is_zero():
            raise Exception(f"direction vector {str(d)} is zero for reflection")
        vc=v.v_res(d)
        v-= vc*(1+ratio)
        return v


    
     # #############
    
    def apply_sva_kinematics(self,ball,dt):
        ball.a=Vector2(0,100)
        oldv=ball.v
        ball.v+=ball.a*dt *0.5
        oldpos=ball.pos
        ball.pos+=((ball.v+oldv)/2)*dt
    
    def apply_all_wall_collosions(self,ball:Ball,oldpos:Vector2):
        bp1,bp2=oldpos,ball.pos

        wl:list[Wall]=self.world.walls
        for wall in wl:

            # wp1,wp2=wall.p1,wall.p2
            # wall=Wall()
            if wall.v_dir.is_zero():
                # if is a point wall, reflect off as a point and ignore other collision checks
                b_v_c=ball.pos-wall.p2
                if (b_v_c).magnitude() <= ball.r:
                    ball.pos=oldpos
                    ball.v = self.reflect_v(ball.v,b_v_c,wall.bounce_factor)
                continue
                

            nd1=wall.dist_from_wall(bp1)
            nd2=wall.dist_from_wall(bp2)
            if sign(nd1) != sign(nd2) or abs(nd1)<ball.r or abs(nd2)<ball.r:
                # if ball will cross unbounded line

                # wall p1 to ball
                v:Vector2=ball.pos-wall.p1

                # - <- P1 0 -> P2 +
                d_along_wall = v.scalar_res(wall.v_dir)

                if in_range(d_along_wall,0,wall.lengh):
                    # reflect velocity vector perpendicular to wall
                    ball.pos=oldpos
                    ball.v = self.reflect_v(ball.v,wall.v_norm,wall.bounce_factor)

                
                elif in_range(d_along_wall,-ball.r,0):
                    # reflect from end of p1
                    b_v_c=ball.pos-wall.p1
                    if (b_v_c).magnitude() <= ball.r:
                        ball.pos=oldpos
                        ball.v = self.reflect_v(ball.v,b_v_c,wall.bounce_factor)
                        
                        
                
                elif in_range(d_along_wall-wall.lengh,0,ball.r):
                    # reflect from end of p2
                    b_v_c=ball.pos-wall.p2
                    if (b_v_c).magnitude() <= ball.r:
                        ball.pos=oldpos
                        ball.v = self.reflect_v(ball.v,b_v_c,wall.bounce_factor)

    def apply_ball_ball_collision(self,ball:Ball,ball2:Ball,op1:Vector2,op2:Vector2):
        dist=(ball.pos - ball2.pos).magnitude()
        r_total=ball.r+ball2.r
        
        if dist<r_total:
            # if ball to ball collision
            # snap back
            d_pv:Vector2=ball.pos-ball2.pos
            ball.pos=op1
            ball2.pos=op2
            
            # old (placeholder, collision mech to replace later)
            
            tbl=[ball,ball2]
            for tempball in tbl:
                if not tempball.fixed:
                    # print("\n")
                    # print(tempball,ball2)
                    # print(d_pv)
                    tempball.v=self.reflect_v(tempball.v,d_pv,tempball.bounce_factor)



            # velocity of ball relative to ball2
            # relative_v=ball.v-ball2.v
            # tangent_rv=relative_v.v_res(d_pv)
            # norm_rv=relative_v-tangent_rv

            # dv=norm_rv/2 *


    def tstep(self,dt):
        bl:list[Ball]=self.world.balls
        obl=[v.copy() for v in bl]

        for i ,ball in enumerate(bl):
            if not ball.fixed:
                self.apply_sva_kinematics(ball,dt)
        
        for i ,ball in enumerate(bl):
            if not ball.fixed:
                oldpos=obl[i].pos
                self.apply_all_wall_collosions(ball,oldpos)
        
        nballs=len(bl)
        for i1 in range(nballs-1):
            for i2 in range(i1+1,nballs):
                ball1=bl[i1]
                ball2=bl[i2]
                op1=obl[i1].pos
                op2=obl[i2].pos
                self.apply_ball_ball_collision(ball1,ball2,op1,op2)



class World:
    def __init__(self,dim:tuple):
        self.dim=dim

        self.walls:list[Wall]=[]
        self.balls:list[Ball]=[]

        self.physics=Physics(self)
    
    def polygon_wall(self,l_nodes):
        
        for i in range(len(l_nodes)-1):
            p1,p2=l_nodes[i:i+2]
            self.walls.append(Wall(p1,p2))

    def add_ball(self,ball:Ball):
        self.balls.append(ball)
    
    def add_wall(self,wall:Wall):
        self.walls.append(wall)
    
    def edge_walls(self):
        l=[(0,0),(self.dim[0],0),self.dim,(0,self.dim[1]),(0,0)]
        self.polygon_wall([Vector2.to_V2(t) for t in l])
        # print([str(w) for w in self.walls])

    def get_walls(self,obj):
        return self.walls
    
    def tstep(self,dt):
        self.physics.tstep(dt)
    