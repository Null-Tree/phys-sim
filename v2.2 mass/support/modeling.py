
# if __name__ == "__main__":
#     from dataclasses import *
# else:
#     from .dataclasses import *

# DEBUG
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
    __slots__=["pos","v","a","r","mass","restitution","oldpos","id","potential_phasing","debug_info"]
    def __init__(self,pos,v=(0,0),a=(0,0),
                 r:int=3,mass:int=None,
                 restitution:float=1):


        self.pos=Vector2.to_V2(pos)
        self.v=Vector2.to_V2(v)
        self.a=Vector2.to_V2(a)
        
        self.r=r
        self.mass=mass if mass != None else r**2
        
        self.restitution = restitution

        
        # for other stuff to meddle with
        self.oldpos=pos
        self.id=None

        self.debug_info=""
    
    def copy(self):
        """obtains a copy of ball"""
        return Ball(self.pos,self.v,self.a,self.r,self.mass,self.restitution)
    
    def __str__(self):
        """enables print() use"""
        return f"Ball({self.pos},{self.v})"


        

class Wall:
    def __init__(self,p1,p2,friction:float=0):
        """p1p2 vector likes, frct def 0"""
        self.p1=Vector2.to_V2(p1)
        self.p2=Vector2.to_V2(p2)
        
        del p1,p2

        self.lengh=(self.p1-self.p2).magnitude()
        

        # direction vectr
        # P1 -> P2
        self.v_dir:Vector2=self.p2-self.p1
        # normal vector
        self.v_norm=Vector2(self.v_dir.y,-self.v_dir.x)

        self.friction=friction

        self.point_wall_bool = (self.v_dir).is_zero()

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
    
     # #############

    
    
    def apply_sva_kinematics(self,ball:Ball,dt):
        """
        applies velocity and acceleration to a ball
        
        :param ball: the ball
        :type ball: Ball
        :param dt: delta time, change in time since last simulated update
        """
        # ball.a=Vector2(0,100)
        oldv=ball.v.copy()
        ball.v+=ball.a*dt

        ball.oldpos=ball.pos.copy()

        # suvat, s=(u+v)/2 * t
        ball.pos+=((ball.v+oldv)/2)*dt

    def ball_potential_speedphasing_test(self,ball:Ball):
        if ball.oldpos==ball.pos: 
            ball.potential_phasing= False
            return

        est_diff_in_p=(ball.pos-ball.oldpos).manh_dist()
        # if we consider its diagnal displacement, can it potentially skip walls
        # yes it would be 2r and we only check new pos
        # return if its next jump will jump over ball diameter
        ball.potential_phasing= (est_diff_in_p >= ball.r*2)

    def point_wall_1ball_bounce(self,ball:Ball,wallpoint:Vector2,override_check=None):
        """wall of zero lengh and 1 ball bounce mechanic"""
        if override_check or (ball.pos-wallpoint).magnitude()<ball.r:
            # snapback
            ball.pos=ball.oldpos
            # reflect
            ball.v = ball.v.reflect_v(ball.pos-wallpoint,ball.restitution)

    def point_wall_1ball_bounce_heavyalgerbaic(self,ball:Ball,wallpoint:Vector2):
        """wall of zero lengh and 1 ball bounce mechanic but with heavy math"""
        # draw a line between 2 ball positions, find closest dist from ball line to wall

        bp1,bp2=ball.oldpos,ball.pos

        bp1_to_wall:Vector2=wallpoint-bp1
        bp1_to_bp2:Vector2=bp2-bp1

        if in_range(bp1_to_wall.scalar_res(bp1_to_bp2),0,bp1_to_bp2.magnitude()):
            shortest_path=bp1_to_wall.norm_v_res(bp1_to_bp2)
            # ball path to wall
            shortest_path_mag_sqr=shortest_path.mag_sqr()
            if shortest_path_mag_sqr <= ball.r ** 2:
                # will contact betweel old pos and new pos but whrer

                print(shortest_path_mag_sqr**0.5)
                
                # see collision pointwall and ball drawing in project folder obsidian
                contact_point_to_wall_resalong_bp1bp2=math.sqrt(ball.r**2 - shortest_path_mag_sqr)
                bp1_to_wall_sres_to_bp2=bp1_to_wall.scalar_res(bp1_to_bp2)
                contact_point = bp1+bp1_to_bp2.scale_to_mag(bp1_to_wall_sres_to_bp2-contact_point_to_wall_resalong_bp1bp2)
                

                # refl ball
                # snap to wall
                wall_to_contactpoint=contact_point-wallpoint
                # ball.pos=wallpoint + (wall_to_contactpoint).scale_to_mag(ball.r+10)

                ball.pos=contact_point + (wall_to_contactpoint).scale_to_mag(1)

                # ball.pos=ball.oldpos


                # refl normal momentum
                ball.v = ball.v.reflect_v(wall_to_contactpoint,ball.restitution)

                # ball.v=Vector2(0,0)

    
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
        if not ball.potential_phasing:
            w_id_l1=set(self.world.wall_base.get_all_adj_chunk_items(bp1,True))
            w_id_l2=set(self.world.wall_base.get_all_adj_chunk_items(bp2,True))
            w_id_l=set.union(w_id_l1,w_id_l2)
            del w_id_l1
            del w_id_l2

            pointwall_bouncer_function=self.point_wall_1ball_bounce
        else:
            w_id_l=set([])
            for pos in self.world.point_raycast_for_chunks(bp1,bp2):
                w_id_l=w_id_l.union(set(self.world.wall_base.get_all_adj_chunk_items(pos,True)))

            pointwall_bouncer_function=self.point_wall_1ball_bounce_heavyalgerbaic

        for w_id in w_id_l:
            wall:Wall=self.world.walls[w_id]

            # DEBUG
            # wall=Wall()

            if wall.v_dir.is_zero():
                # if is a point wall, reflect off as a point and ignore other collision checks
                pointwall_bouncer_function(ball,wall.p1)
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
                    ball.v = ball.v.reflect_v(wall.v_norm,ball.restitution)
                    return

                

            # note this should only run if we are already sure ball wont bounce off a mid section not an end section 
            for wallp in [wall.p1,wall.p2]:
                pointwall_bouncer_function(ball,wallp)

    # TODO make collisions account retisity
    # TODO make collisions for potenetial phasers
    def apply_all_ball_collosions(self,ball:Ball):

        """
        applies ball collision for a single ball (if nessicary)
        
        :param ball: ball1
        :type ball: Ball

        """

        # for intellesense only DEBUG
        # self.world=World()
        # self.world.create_chunkbases()

        if not ball.potential_phasing:
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
                                
                if dist_sqr<=r_total**2:
                    # if ball to ball collision
                    
                    # snap back
                    ball.pos=op1
                    ball2.pos=op2
                    
                    # Find velocity lose
                    v_lost_by_ball1=ball.v.v_res(d_pv)
                    v_lost_by_ball2=ball2.v.v_res(d_pv)

                    #remove velocity to be swapped
                    ball.v-= v_lost_by_ball1
                    ball2.v -= v_lost_by_ball2


                    # swap velocities with acknowedgemtn of weight
                    ball.v += (v_lost_by_ball2 * ball2.mass) / ball.mass
                    ball2.v+= (v_lost_by_ball1 * ball.mass) / ball2.mass

        else:
            # if potential phasing
            raise Exception("not made yet lol")
        
    
    def apply_all_gravity(self):
        for i1,ball1 in enumerate(self.world.balls):
            ball1.a=Vector2(0,0)
            for i2,ball2 in enumerate(self.world.balls):    
                if i1!=i2:
                    v_toBall2:Vector2=ball2.pos - ball1.pos
                    strengh=self.world.g_coef * (ball1.mass * ball2.mass) / (v_toBall2.mag_sqr()) / ball1.mass
                    ball1.a +=  v_toBall2.unit_v() * strengh


    def tstep_physics(self,dt):
        """
        takes a step in time
        does svakinematics, wallball and ballball collisions
        
        :param dt: dt
        """
        bl:list[Ball]=self.world.balls
        obl=[v.copy() for v in bl]

        
        for i ,ball in enumerate(bl):
            self.ball_potential_speedphasing_test(ball)

        for i ,ball in enumerate(bl):
            self.apply_all_wall_collosions(ball)
        
        for i ,ball in enumerate(bl):
            self.apply_all_ball_collosions(ball)

        for i ,ball in enumerate(bl):
            self.apply_all_gravity()
        
        for i ,ball in enumerate(bl):
            self.apply_sva_kinematics(ball,dt)

        if self.world.gameobj.show_ball_id:

            for ball in bl:
                # ball.debug_info=str(ball.mass)
                ball.debug_info=str(f"{ball.id}: {(self.world.ball_base.get_all_adj_chunk_items(ball.pos,True))}")


        
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
        """Clears chunkbase of all contents"""
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
        """Checks if a chunk cord is inbounds of the chunkbase"""
        x,y=v.as_tup()
        if in_range(x,0,self.cdim[0]-1) and in_range(y,0,self.cdim[1]-1):
            return True
        return False

    
    # EDIT

    def add_id(self,value,inw_p:Vector2):
        """
        Adds an id to chunkbase
        
        :param value: data to add to chunkbase
        :param inw_p: inworld position vector of object
        :type inw_p: Vector2
        """

        c_pos=self.get_chunk_cord(inw_p)
        if self.is_chunk_cord_inbounds(c_pos):
            i1,i2=c_pos.as_tup()
            self.arr[i1][i2].add(value)
        else:
            self.outside.add(value)
    
    def get_adj_chunk_cords(self,cc:Vector2):
        """gets all adj chunk cords"""
        dl=[-1,0,1]
        out=[]
        for dx in dl:
            for dy in dl:
                ncc=cc+Vector2(dx,dy)
                if self.is_chunk_cord_inbounds(ncc):
                    out.append(ncc)
        
        return out


    def get_all_adj_chunk_items(self,inw_p:Vector2,include_outside=True):
        """gets all adj chunk items"""
        chunk_c=self.get_chunk_cord(inw_p)
        # del inw_p
        
        if not self.is_chunk_cord_inbounds(chunk_c):
            print(f"OUTSIDE???: {chunk_c}.{inw_p}")
            return list(self.outside)

        ccl=self.get_adj_chunk_cords(chunk_c)


        adj_items=set()
        for cc in ccl:
            for v in self[cc]:
                adj_items.add(v)

        if include_outside:
            output=set.union(adj_items,self.outside)
        else:
            output=adj_items


        
        return list(output)



class World:
    """handles storage of objects in world, 1 per game"""
    def __init__(self,dim:tuple,max_ball_radius:int=50,g_coef:int=0,gameobj=None):
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

        self.last_ball_created=None

        self.g_coef=g_coef
    
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
        """update ball position in chunkbase"""
        self.ball_base.clear()
        for i,ball in enumerate(self.balls):
            ball.id=i
            self.ball_base.add_id(i,ball.pos)

    def point_raycast_for_chunks(self,p1:Vector2,p2:Vector2):
        points=[p1,p2]
        diff=p2-p1
        
        mag=diff.magnitude()

        if mag!=0:
            unit=self.wall_base.side_len//5
            n_segs=mag//unit
            if n_segs !=0:
                sub_diff= diff/n_segs
                interm_node=p1
                for _ in range(0,math.floor(n_segs)):
                    interm_node+=sub_diff
                    points.append(interm_node)
        return points
    



    def update_single_wall_chunk(self,i):
        """creates the chunkbase entries for a wall"""
        #  is index of wall in self.walls
        wall:Wall=self.walls[i]

        for p in self.point_raycast_for_chunks(wall.p1,wall.p2):
            self.wall_base.add_id(i,p)    

            



    def update_wall_chunks(self):
        """update all walls in chunkbase, additive not reset"""
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

    def add_ball(self,ball:Ball=None):
        """adds ball obj to world, if ball not provided uses last ball"""
        if ball == None:
            if self.last_ball_created:
                ball=self.last_ball_created
            else:
                return

        self.last_ball_created=ball.copy()
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


   
        
    