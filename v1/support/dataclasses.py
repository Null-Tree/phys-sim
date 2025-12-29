import math
import random


class Vector2:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def as_list(self):
        return [self.x,self.y]
    
    def as_tup(self):
        return (self.x,self.y)
    
    def copy(self):
        n=Vector2(self.x,self.y)
        return n

    def __str__(self):    
        return f"{self.__class__.__name__}({self.x},{self.y})"
    

    def round(self,n):
        return Vector2(round(self.x,n),round(self.y,n))
    
    def to_V2(v):
        t=type(v)
        if t == Vector2:
            return v
        elif t in [list,tuple] and len(v) ==2:
            return Vector2(v[0],v[1])
        else:
            raise Exception(f"data {t}({v}) not supported with vector2")
    
    def random():
        return Vector2(random.random(),random.random())
    
    def is_zero(self):
        if self.x==0 and self.y==0:
            return True
        return False

        
    def __eq__(self, v):
        t=type(v)
        if t not in [Vector2,list,tuple]:
            return False

        v=Vector2.to_V2(v)
        if self.x==v.x and self.y==v.y:
            return True
        return False
    
    def __neq__(self,v):
        return not (self==v)

    def __add__(self,v2):
        v2=Vector2.to_V2(v2)
        return Vector2(self.x + v2.x, self.y + v2.y)
    
    def __sub__(self,v2):
        v2=Vector2.to_V2(v2)
        return Vector2(self.x - v2.x, self.y - v2.y)
    
    def scalar_mul(self,c):
        return Vector2(c*self.x,c*self.y)
    
    def dot_p(self,v2):
        return self.x*v2.x + self.y*v2.y
    
    def __mul__(self,q):
        t=type(q)
        if t in [float,int]:
            return self.scalar_mul(q)
        if t in [Vector2,list,tuple]:
            v2=Vector2.to_V2(q)
            return self.dot_p(v2)
    
    def __truediv__(self,c):
        if type(c) not in [int,float]:
            raise Exception("invalid data type for division")
        else :
            return Vector2(self.x/c,self.y/c)
    
    def __floordiv__(self,c):
        if type(c) not in [int,float]:
            raise Exception("invalid data type for division")
        else :
            return Vector2(self.x//c,self.y//c)
    
    def magnitude(self):
        m=(self.x**2 + self.y**2)**0.5
        # print(type(m))
        return m
    
    def mag_sqr(self):
        return (self.x**2 + self.y**2)

    
    def unit_v(self):
        uv=self/self.magnitude()
        return uv
    
    def scalar_res(self,d):
        d=Vector2.to_V2(d)
        unitd=d.unit_v()
        return self * unitd

    def v_res(self,d):
        d=Vector2.to_V2(d)
        if d.is_zero():
            raise Exception("direction vector is zero (for vres)")
        unitd=d.unit_v()
        return unitd*(self * unitd)
    
    def ang(self,v2,mode="rad"):
        """returns in either rad (default) or deg"""
        v2=Vector2.to_V2(v2)
        dot=(self*v2) / (self.magnitude() * v2.magnitude())
        
        rad= math.acos(dot)
        if mode =="rad":
            return rad
        if mode =="deg":
            return rad/math.pi * 180
        

if __name__ == "__main__":    
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

        