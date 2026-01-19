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
        self.oldpos=p
        self.id=None
    
    def copy(self):
        """obtains a copy of ball"""
        return Ball(self.pos,self.v,self.a,self.r)
    
    def __str__(self):
        """enables print() use"""
        return f"Ball({self.pos},{self.v})"

class Wall:
    def __init__(self,p1:Vector2,p2:Vector2,bounce_factor=.8):
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
    
    def apply_sva_kinematics(self,ball:Ball,dt):
        """
        applies velocity and acceleration to a ball
        
        :param ball: the ball
        :type ball: Ball
        :param dt: delta time, change in time since last simulated update
        """
        # ball.a=Vector2(0,100)
        oldv=ball.v
        ball.v+=ball.a*dt *0.5
        ball.oldpos=ball.pos
        ball.pos+=((ball.v+oldv)/2)*dt
    
    def apply_all_wall_collosions(self,ball:Ball):
        """
        applies all relevant wall collisions for a given ball 
        
        :param ball: the ball object
        :type ball: Ball

        """
        oldpos=ball.oldpos
        bp1,bp2=oldpos,ball.pos

        # for intellesense only DEBUG
        # self.world=World()
        # self.world.create_chunkbases()


        w_id_l1=self.world.wall_base.get_all_adj_chunk_items(bp1,True)
        w_id_l2=self.world.wall_base.get_all_adj_chunk_items(bp2,True)
        
        w_id_l=set(w_id_l1 + w_id_l2)

        del w_id_l1
        del w_id_l2


        wl=[self.world.walls[wid] for wid in w_id_l]


            



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

    def apply_all_ball_collosions(self,ball:Ball):
        """
        applies ball collision for a single ball (if nessicary)
        
        :param ball: ball1
        :type ball: Ball

        """

        # for intellesense only DEBUG
        # self.world=World()
        # self.world.create_chunkbases()

        op1=ball.oldpos


        # # uses both positions
        # b_id_l1=self.world.ball_base.get_all_adj_chunk_items(op1,True)
        # b_id_l2=self.world.ball_base.get_all_adj_chunk_items(ball.pos,True)
        # b_id_l=set(b_id_l1 + b_id_l2)
        # del b_id_l1
        # del b_id_l2
        # bl:list[Ball]=[self.world.balls[bid] for bid in b_id_l]

        b_id_l=(self.world.ball_base.get_all_adj_chunk_items(ball.pos,True))
        if ball.id not in b_id_l:
            print("ball could not detect self",ball.id,self.world.ball_base.get_chunk_cord(ball.pos))
            pass
        else:
            b_id_l.remove(ball.id)

        bl:list[Ball]=[self.world.balls[bid] for bid in b_id_l]

        # DEBUG
        
        # print("f")
        # self.world=World()
        # from .graphics import Game
        # self.world.gameobj=Game()
        # Game.draw_line

        # self.world.gameobj.place_text(str(len(bl)),self.world.gameobj.world_to_screen_v(ball.pos),(0,100,0))


        for ball2 in bl:
            # self.world.gameobj.draw_line(ball.pos,ball2.pos,(0,0,100),1,True)
            
            # print("lined")
            # print(ball.id,[v for v in b_id_l])





            op2=ball2.oldpos
            d_pv:Vector2=ball.pos-ball2.pos

            r_total=ball.r+ball2.r

            diag_d=d_pv.x + d_pv.y
            if diag_d > 2*r_total:
                continue

            

            dist_sqr=(ball.pos - ball2.pos).mag_sqr()
            
            
            if dist_sqr<r_total**2:
                # dist=dist_sqr**0.5
                # if ball to ball collision
                # snap back
                
                ball.pos=op1
                ball2.pos=op2
                

                # swap velocities along the dir vector
                dv1=ball.v.v_res(d_pv)
                dv2=ball2.v.v_res(d_pv)
                
                ball.v += dv2-dv1
                ball2.v+= dv1-dv2

    def tstep_physics(self,dt):
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
                self.apply_all_wall_collosions(ball)
        
        for i ,ball in enumerate(bl):
            if not ball.fixed:
                self.apply_all_ball_collosions(ball)
        
class Chunk_Base:
    """
    Notes
    due to how edges are
    positions on very border eg (50,50) need to be included onto adjacent edge
    """

    __slots__=["arr","cdim","side_len","outside"]
    
    # CREATION
    def create_matrix(cdim):
        """creates a matrix of lists by cdim"""
        xc=cdim[0]
        yc=cdim[1]
        return [[set() for y in range(yc)] for x in range(xc)]

    def __init__(self,cdim:tuple,side_len:int):
        """
        Creates a chunkbase
        
        :param self: Description
        :param cdim: chunk dimensions
        :type cdim: tuple[2]
        :param side_len: px inworld sidelengh of a chunk
        """
        self.cdim=cdim
        self.arr = Chunk_Base.create_matrix(cdim)
        self.side_len=side_len
        self.outside=set()
    
    # DEBUG
    def heatmap(self):
        """heatmap of chunkbase with numbers being number of obj in chunk"""

        return [[len(c) for c in r] for r in self.arr]

    def __str__(self,item_delim="  ", row_delim="\n",maxl_mode="all"):
        
        # enables pring

        print_arr=self.heatmap()


        maxl=0
        for row in print_arr:
            for v in row:
                maxl=max(maxl,len(str(v)))
        
        maxl=maxl 
        str_l=[]
        for row in print_arr:
            rowl=[]
            for col_i,v in enumerate(row):
                rowl.append(str(v).rjust(maxl))
            str_l.append(item_delim.join(rowl))
                     
        return row_delim.join(str_l) + f"\n Outside: {len(self.outside)}\n"

    # RESET
    
    def clear(self):
        self.arr:list[list[set]] = Chunk_Base.create_matrix(self.cdim)
        self.outside=set()

    # GET
    
    def __getitem__(self,chunk_c) -> tuple:
        """
        gets the list of chunk for a chunk cordinate
        
        :param chunk_c: chunk cordinate
        :type chunk_c: tuple[2], Vector2
        """
        if type(chunk_c) == Vector2:
            chunk_c=chunk_c.as_tup()
        # print(chunk_c)
        return tuple(self.arr[chunk_c[0]][chunk_c[1]])

    
    def get_chunk_cord(self,inw_p:Vector2):
        """
        gets chunk cordinates as a tuple for a given position inworld
        
        :param inw_p: inworld position
        :type inw_p: Vector2
        """

        # if on border

        return (inw_p // self.side_len).to_int()
    
    
    
    def is_chunk_cord_inbounds(self,v:Vector2):
        x,y=v.as_tup()
        if in_range(x,0,self.cdim[0]-1) and in_range(y,0,self.cdim[1]-1):
            return True
        return False

    
    # EDIT

    def add_id(self,value:Vector2,inw_p:Vector2):

        c_pos=self.get_chunk_cord(inw_p)
        if self.is_chunk_cord_inbounds(c_pos):
            i1,i2=c_pos.as_tup()
            self.arr[i1][i2].add(value)
        else:
            self.outside.add(value)
    
    def get_adj_chunk_cords(self,cc:Vector2):
        dl=[-1,0,1]
        out=[]
        for dx in dl:
            for dy in dl:
                ncc=cc+Vector2(dx,dy)
                if self.is_chunk_cord_inbounds(ncc):
                    out.append(ncc)
        
        return out



    def get_all_adj_chunk_items(self,inw_p:Vector2,include_outside=True):
        chunk_c=self.get_chunk_cord(inw_p)
        # del inw_p
        
        if not self.is_chunk_cord_inbounds(chunk_c):
            print(f"OUTSIDE???: {chunk_c}.{inw_p}")
            return list(self.outside)

        if include_outside:
            output=set(self.outside)
        else:
            output=set()

        ccl=self.get_adj_chunk_cords(chunk_c)
        

        for cc in ccl:
            for v in self[cc]:
                output.add(v)
        
        
        return list(output)


class World:
    """handles storage of objects in world, 1 per game"""
    def __init__(self,dim:tuple,max_ball_radius:int=50,gameobj=None):
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

        self.max_ball_radius=max_ball_radius

        self.create_chunkbases()

        self.gameobj=gameobj
    
    # CHUNKING

    def create_chunkbases(self):
        """creates chunk base for World based on max ball size"""
        
        chunk_side_lengh=int(self.max_ball_radius * 1.1 +10 ) * 2                  

        cdim=tuple([math.ceil(v/chunk_side_lengh) for v in self.dim])

        self.wall_base=Chunk_Base(cdim,chunk_side_lengh)
        self.ball_base=Chunk_Base(cdim,chunk_side_lengh)

        self.update_ball_chunks()
        self.update_wall_chunks()
    
    def update_ball_chunks(self):
        self.ball_base.clear()
        for i,ball in enumerate(self.balls):
            ball.id=i
            self.ball_base.add_id(i,ball.pos)




    def update_single_wall_chunk(self,i):
        #  is index of wall in self.walls
        wall:Wall=self.walls[i]

        
        diff=wall.p2-wall.p1
        
        mag=diff.magnitude()

        unit=self.wall_base.side_len//5

        n_segs=mag//unit

        sub_diff= diff/n_segs

        interm_node=wall.p1
        for _ in range(0,math.floor(n_segs)):
            interm_node+=sub_diff
            self.wall_base.add_id(i,interm_node)
        
        self.wall_base.add_id(i,wall.p2)

            



    def update_wall_chunks(self):
        for i in range(len(self.walls)):
            self.update_single_wall_chunk(i)

    


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
        id=len(self.balls)
        ball.id=id
        self.balls.append(ball)
        self.ball_base.add_id(id,ball.pos)
    
    def add_wall(self,wall:Wall):
        """adds a wall object to world"""
        i=len(self.walls)
        self.walls.append(wall)
        self.update_single_wall_chunk(i)
    
    def edge_walls(self):
        """creates walls at end of world"""
        if not self.boundary_walled:
            l=[(0,0),(self.dim[0],0),self.dim,(0,self.dim[1]),(0,0)]
            self.polygon_wall([Vector2.to_V2(t) for t in l])
            # print([str(w) for w in self.walls])
            self.boundary_walled=True
            self.update_wall_chunks()
    
    def clear(self,clearboundary=True):
        """clear world of everything"""
        self.walls=[]
        self.balls=[]
        if clearboundary:
            self.boundary_walled=False
        else:
            self.edge_walls()
        
        self.ball_base.clear()
        self.wall_base.clear()
        self.update_wall_chunks()
        self.update_ball_chunks()

    def get_walls(self,obj):
        
        return self.walls
    
    def tstep(self,dt):
        self.update_ball_chunks()
        self.physics.tstep_physics(dt)


   
        
    