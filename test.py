
class Vector2:
    """
    Docstring for Vector2
    2D Vector class

    note: x is right, y is down
    
    
    """

    __slots__=["x","y"]
    
    def __init__(self,x,y):
        """
        Initalises a vector2 object
        
        :param x: x cordinate
        :type x: int,float
        :param y: y cordinate
        :type y: int,float, 
        """
        self.x=x
        self.y=y
    
    def to_int(self):
        self.x=int(self.x)
        self.y=int(self.y)
        return self

    def as_list(self):
        """
        returns x y cordinates as a list [x,y]
        """
        return [self.x,self.y]
    
    def as_tup(self):
        """
        returns x y cordinates as a tuple (x,y)
        """
        return (self.x,self.y)
    
    def copy(self):
        """
        returns a copy of the vector
        """
        n=Vector2(self.x,self.y)
        return n

    def __str__(self):    
        """
        str convert, use for compatability with print()
        """
        return f"{self.__class__.__name__}({self.x},{self.y})"
    

    def round(self,n):
        """
        Rounds x and y to n decimal places
        
        :param n: dc place
        :type n: int
        """
        return Vector2(round(self.x,n),round(self.y,n))
    
    def to_V2(v):
        """
        Converts a vectorlike element to a vector2 class
        """
        t=type(v)
        if t == Vector2:
            return v
        elif t in [list,tuple] and len(v) ==2:
            return Vector2(v[0],v[1])
        else:
            raise Exception(f"data {t}({v}) not supported with vector2")
    
    def random():
        """
        obtains a random vector with xy between 0 n 1
        """
        return Vector2(random.random(),random.random())
    
    def is_zero(self):
        """
        Checks if both x and y are zero
        """
        if self.x==0 and self.y==0:
            return True
        return False

        
    def __eq__(self, v):
        """
        checks if Vectors are equal
       """
        t=type(v)
        if t not in [Vector2,list,tuple]:
            return False

        v=Vector2.to_V2(v)
        if self.x==v.x and self.y==v.y:
            return True
        return False
    
    def __neq__(self,v):
        """checks if not equal"""
        return not (self==v)

    def __add__(self,v2):
        """
        Adds Vector and vectorlike objects
        """
        v2=Vector2.to_V2(v2)
        return Vector2(self.x + v2.x, self.y + v2.y)
    
    def __sub__(self,v2):
        """
        subtracts Vector and vectorlike objects
        """
        v2=Vector2.to_V2(v2)
        return Vector2(self.x - v2.x, self.y - v2.y)
    
    def scalar_mul(self,c):
        """
        multiplies Vector and a scalar numeric
        :param c: scalar numeric
        :type c: int,float
        """
        return Vector2(c*self.x,c*self.y)
    
    def dot_p(self,v2):
        """
        vector dot product between vector and vectorlike
        :param v2: second vector
        :type v2: Vector2, list[2], tuple[2]
        """
        v2=Vector2.to_V2(v2)
        return self.x*v2.x + self.y*v2.y
    
    def __mul__(self,q):
        """dynamic use of dot_p and scalar_mul dep on datatype of q"""
        t=type(q)
        if t in [float,int]:
            return self.scalar_mul(q)
        if t in [Vector2,list,tuple]:
            v2=Vector2.to_V2(q)
            return self.dot_p(v2)
    
    def __truediv__(self,c):
        """true div by scalar numeric"""
        if type(c) not in [int,float]:
            raise Exception("invalid data type for division")
        else :
            return Vector2(self.x/c,self.y/c)
    
    def __floordiv__(self,c):
        """floor div by scalar numeric"""
        if type(c) not in [int,float]:
            raise Exception("invalid data type for division")
        else :
            return Vector2(self.x//c,self.y//c)
    
    def magnitude(self):
        """gets magnitude of vector"""
        m=(self.x**2 + self.y**2)**0.5
        # print(type(m))
        return m
    
    def mag_sqr(self):
        """mag **2"""
        return (self.x**2 + self.y**2)

    
    def unit_v(self):
        """obtains unit vector of a vector"""
        uv=self/self.magnitude()
        return uv
    
    def scalar_res(self,d):
        """
        obtain scalar res with a vectr like
        :param d: direction vector
        :type d: Vector2, list[2], tuple[2]
        """
        d=Vector2.to_V2(d)
        unitd=d.unit_v()
        return self * unitd

    def v_res(self,d):
        """
        obtain vector res with a vector like
        
        :param d: direction vector
        :type d: Vector2, list[2], tuple[2]
        """
        d=Vector2.to_V2(d)
        if d.is_zero():
            raise Exception("direction vector is zero (for vres)")
        unitd=d.unit_v()
        return unitd*(self * unitd)
    
    def ang(self,v2,mode="rad"):
        """
        Obtains angle with another vectorlike

        :param v2: the vectorlike
        :type v2: Vector2, list[2], tuple[2]
        :param mode: default radians, use "rad" or "deg" for respective mode
        
        """
        # returns in either rad (default) or deg"""
        
        v2=Vector2.to_V2(v2)
        dot=(self*v2) / (self.magnitude() * v2.magnitude())
        
        rad= math.acos(dot)
        if mode =="rad":
            return rad
        if mode =="deg":
            return rad/math.pi * 180
     
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

        print([(cc.as_tup()) for cc in ccl])
        

        for cc in ccl:
            for v in self[cc]:
                output.add(v)
        
        
        return list(output)
 

def main():
    cc=Chunk_Base((4,4),100)
    # adj_c_l=(cc.get_adj_chunk_cords(Vector2(1,1)))
    # for c in adj_c_l:
    #     # c=Vector2()
    #     print(c.as_tup())

    for i in range(3):
        for j in range(3):
            c=Vector2(50,50) + Vector2(100*i,100*j)
            cc.add_id(f"{i}-{j}",c)
    
    print(cc)

    r=cc.get_all_adj_chunk_items(Vector2(1,201))
    print(r)
main()