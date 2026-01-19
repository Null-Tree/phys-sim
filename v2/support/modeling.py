from .dataclasses import *



def sign(v):
    """gets sign of a value as a signed unit 1"""
    if v >0:
        return 1
    if v<0:
        return-1
    if v==0:
        return 0

def in_range(v,min,max):
    """
    checks if a value is between 2 other values

    :param v: value
    :param min: 
    :param max: 
    """
    """inrange inclusive"""
    if v >= min and v <= max:
        return True
    return False

class Ball:
    
    def __init__(self,p,v=(0,0),a=(0,0),r:int=3,bounce_factor:float=1,fixed:bool=False):
        """
        creates a ball object
        
        :param p: position
        :type p: Vector2,list[2],tuple[2]

        :param v: Velocity
        :type p: Vector2,list[2],tuple[2]

        :param a: acceleration
        :type p: Vector2,list[2],tuple[2]

        :param r: radius
        :type r: int

        :param bounce_factor: how much velocity to remain after bounce with other balls ONLY, TODO NOT CURRENTLY IMPLEMENTED

        :type bounce_factor: float
        :param fixed: will the ball be stationary permanently
        :type fixed: bool
        """
        self.pos=Vector2.to_V2(p)
        self.v=Vector2.to_V2(v)
        self.a=Vector2.to_V2(a)
        self.r=r
        self.fixed=fixed
        self.bounce_factor=bounce_factor
    
    def copy(self):
        """obtains a copy of ball"""
        return Ball(self.pos,self.v,self.a,self.r)
    
    def __str__(self):
        """enables print() use"""
        return f"Ball({self.pos},{self.v})"

class Wall:
    def __init__(self,p1:Vector2,p2:Vector2,bounce_factor=1):
        """
        Creates a wall object
        
        :param p1: position of an end
        :type p1: Vector2
        :param p2: position of other end
        :type p2: Vector2
        :param bounce_factor: how much velocity will balls retain on bounce
        """
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
        """
        Gets shortest distance form a point to wall
        
        :param p: the point
        :type p: Vector2, list[2], tuple[2]
        """
        p=Vector2.to_V2(p)
        v=p-self.p1
        d=v.scalar_res(self.v_norm)
        return d
    

    def __str__(self):
        """enables print()"""
        return f"Wall({str(self.p1)} to {str(self.p2)})"
    




class Physics:
    """stores physics related params and functions, 1 per game"""
    def __init__(self,world):
        """
        creates a physics handler

        :param world: the parent world object
        """
        self.world=world
    
    def p_contact_ball_wall(ball:Ball,wall:Wall):
        "tf is tthis"
        pass

    def reflect_v(self,v:Vector2,d:Vector2,ratio=1):
        """
        for a given vector v and a direction vector d, it will reflect vector component of v paralel to d
        
        :param v: original vector
        :type v: Vector2
        :param d: direction vector (does not have to be unit)
        :type d: Vector2
        :param ratio: how much will the paralel vector component be lost?
        """
        if d.is_zero():
            raise Exception(f"direction vector {str(d)} is zero for reflection")
        d=d.unit_v()
        vc=v.v_res(d)
        v-= vc*(1+ratio)
        return v


    
     # #############
    
    def apply_sva_kinematics(self,ball,dt):
        """
        applies velocity and acceleration to a ball
        
        :param ball: the ball
        :type ball: Ball
        :param dt: delta time, change in time since last simulated update
        """
        # ball.a=Vector2(0,100)
        oldv=ball.v
        ball.v+=ball.a*dt *0.5
        oldpos=ball.pos
        ball.pos+=((ball.v+oldv)/2)*dt
    
    def apply_all_wall_collosions(self,ball:Ball,oldpos:Vector2):
        """
        applies all relevant wall collisions for a given ball 
        
        :param ball: the ball object
        :type ball: Ball
        :param oldpos: the old position of the ball, used to ensure it does not clip accross walls
        :type oldpos: Vector2
        """
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
        """
        applies ball collision between two balls (if nessicary)
        
        :param ball: ball1
        :type ball: Ball
        :param ball2: ball2
        :type ball2: Ball
        :param op1: old position of ball1
        :type op1: Vector2
        :param op2: old position of ball2
        :type op2: Vector2
        """
        
        d_pv:Vector2=ball.pos-ball2.pos

        r_total=ball.r+ball2.r

        diag_d=d_pv.x + d_pv.y
        if diag_d > 2*r_total:
            return

        

        dist_sqr=(ball.pos - ball2.pos).mag_sqr()
        
        
        if dist_sqr<r_total**2:
            # dist=dist_sqr**0.5
            # if ball to ball collision
            # snap back
            
            ball.pos=op1
            ball2.pos=op2
            
            # old (placeholder, collision mech to replace later)
            

            # swap velocities along the dir vector
            dv1=ball.v.v_res(d_pv)
            dv2=ball2.v.v_res(d_pv)
            
            ball.v += dv2-dv1
            ball2.v+= dv1-dv2

    def tstep(self,dt):
        """
        takes a step in time
        does svakinematics, wallball and ballball collisions
        
        :param dt: dt
        """
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

# chuknbase
    
    


class World:
    """handles storage of objects in world, 1 per game"""
    def __init__(self,dim:tuple,max_ball_size:int=50):
        """
        Creates blank world object
        
        :param dim: dimensions of world (x,y) tuple
        :type dim: tuple
        :param max_ball_size: max ball size to use for chunking
        :type max_ball_size: int
        """
        
        self.dim=dim

        # NOTE BECAUSE INDEX is used for ball id, remove ball sby replace with none, or replace this with dict
        self.walls:list[Wall]=[]
        self.balls:list[Ball]=[]

        self.physics=Physics(self)

        self.boundary_walled=False

        self.max_ball_size=max_ball_size

        self.create_chunks()
    
    # CHUNKING

    def create_chunks(self):
        """creates chunk base for World based on max ball size"""
        chunk_side_lengh=self.max_ball_size+10

        nc_dim=tuple([math.ceil(v//chunk_side_lengh) for v in self.dim])


            



    


    # WALL BALL STUFF
    
    def polygon_wall(self,l_nodes:list[Vector2]):
        """
        creates walls between every pair of positions in list, will not connect ends

        :param l_nodes: list of vectors
        :type l_nodes: list[list[Vector2]]
        """
        
        for i in range(len(l_nodes)-1):
            p1,p2=l_nodes[i:i+2]
            self.walls.append(Wall(p1,p2))

    def add_ball(self,ball:Ball):
        """adds ball obj to world"""
        self.balls.append(ball)
    
    def add_wall(self,wall:Wall):
        """adds a wall object to world"""
        self.walls.append(wall)
    
    def edge_walls(self):
        """creates walls at end of world"""
        if not self.boundary_walled:
            l=[(0,0),(self.dim[0],0),self.dim,(0,self.dim[1]),(0,0)]
            self.polygon_wall([Vector2.to_V2(t) for t in l])
            # print([str(w) for w in self.walls])
            self.boundary_walled=True
    
    def clear(self,clearboundary=True):
        """clear world of everything"""
        self.walls=[]
        self.balls=[]
        if clearboundary:
            self.boundary_walled=False
        else:
            self.edge_walls()

    def get_walls(self,obj):
        
        return self.walls
    
    # COPY OF TSTEP
    def tstep(self,dt):
        self.physics.tstep(dt)
    