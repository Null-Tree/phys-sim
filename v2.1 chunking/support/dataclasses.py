import math
import random


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
        

if __name__ == "__main__":  
    import time
    st=  time.time()
    v1=Vector2(1,6)
    v2=Vector2(2,12)

    print(v2+v1)
    print(v2-v1)
    print(v1-v2)
    print(v1+(9,9))
    print(v1*v2)
    print(v1*9)

    print(Vector2(1/3,2/3).round(2))
    print(Vector2(1,2)/3)

    print(v1)
    print(v1==(1,6))
    print(v1!=(1,1))

    r=v1.v_res((1,-8))
    print(r)

    print(v1.ang((1,1)))
    print(v1.ang((1,1),"deg"))
    dt=time.time()-st
    print(dt," elapsed")

        