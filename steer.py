# -*- coding: utf-8 -*- 
import math
import random

class SimpleVehicle:

    def __init__(self, unit):
        self.mass = 1.0
        self.velocity = Vec2(unit.vx. unit.vy)
        self.radius = 150
        self.force = 150
        self.max_speed = 150
        self.position = None
        self.forward = None
        self.side = None

        self.curvature = 1.0
        self.last_forward = None
        self.last_position = None
        self.smoothed_position = None
        self.smoothed_curvature = 1.0
        self.smoothed_acceleration = None

    def predict_future_position(self, prediction_time):
        return self.position.add(self.velocity.mult(prediction_time))        

    def measure_path_curvature(self, elapsed_time):
        
        if elapsed_time > 0:
            
            dP = self.last_position.sub(self.position)
            dF = self.last_forward.sub(self.forward).div(dP.length())

            lateral = dF.perpendicular_component(self.forward)

            sign = 1.0 if lateral.dot(self.side) >= 0  else  -1.0
            curvature = lateral.length() * sign

            lastForward = self.forward
            lastPosition = self.position




class Vec2:
    """Определение вектора для решения задачи по поиску"""
    def __init__(self, x=0.0, y = 0.0):
        self.x,self.y = x,y
        
    def perpendicular_component(self, v):
        return self.sub(self.parallel_component(v))

    def dot(self, v):
        return self.x*v.x + self.y*v.y

    def sub(self, v):
        return Vec2(self.x - v.x, self.y - v.y)

    def minus(self):
        return Vec2(-self.x, -self.y)

    def add(self, v):
        return Vec2(self.x + v.x, self.y + v.y)

    def div(self, scalar):
        return Vec2(self.x/scalar, self.y/scalar)

    def mult(self, scalar):
        return Vec2(self.x*scalar, self.y*scalar)

    def lenght(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        lenght = self.lenght()
        if lenght > 0:
            return self.div(lenght)
        return self

    def cross(self, a):
        self = Vec2(self.y, -self.x)

    def distance(self, v):
        return math.hypot(self.x-v.x, self.y-v.y)

    def parallel_component(self, unit_basis):
        projection = self.dot(unit_basis)
        return unit_basis.mult(projection)

    def truncate_lenght(self, max_length):
        length = self.lenght()
        math.fabs(max_length)

        if (length > math.fabs(max_length)):
            return self.mult( max_length / length)
        return self

    def set_y_zero(self):
        return Vec2(self.x,0)


    def rotate(self, alpha):
        s = math.sin(alpha)
        c = math.cos(alpha)

        return Vec2(self.x*c-self.y*s, self.x*s+self.y*c)

    def angle_to(self, v):
        dot  = self.normalize().dot(v.normalize())
        return math.acos(dot)


    def distance_from_line(self, point, line_origin, line_unit_tangent):
        offset = point.sub(line_origin)
        perp = offset.perpendicular_component(line_unit_tangent)

        return perp.length()

    def __repr__(self):
        return "Vec2"

    def __str__(self):
        return "(%f,%f)" % (self.x,self.y)



    def random_vector_in_unit_radius(self):
        """Returns a position randomly distributed on a disk of unit radius
    on the XZ (Y=0) plane, centered at the origin.  Orientation will be
    random and length will range between 0 and 1"""
        find_solution = False
        while(not find_solution):
            v = Vec2(random.random()*2-1,random.random()*2-1)
            find_solution = v.lenght() >= 1

        return v

    def random_unit_vector(self):
        """
        Returns a position randomly distributed on the surface of a sphere
        of unit radius centered at the origin.  Orientation will be random
        and length will be 1"""
        return self.random_vector_in_unit_radius().normilize()


    def vec_limit_deviation_angle_utility(self,insideOrOutside,source,cosineOfConeAngle,basis):
        sourceLength = source.length()

        if (sourceLength == 0): 
            return source

        direction = source.div(sourceLength)
        cosineOfSourceAngle = direction.dot (basis)

        if insideOrOutside:
            if cosineOfSourceAngle >= cosineOfConeAngle:
                return source
        else:
            if cosineOfSourceAngle <= cosineOfConeAngle:
                return source

        perp = source.perpendicular_component(basis)
        unitPerp = perp.normalize()

        perpDist = math.sqrt(1 - cosineOfConeAngle*cosineOfSourceAngle)

        c0 = basis.mult(cosineOfConeAngle)
        c1 = unitPerp.mult(perpDist)

        return c0.add(c1).mult(sourceLength)



    def limit_max_deviation_angle(self,source,cosineOfConeAngle,basis):
        return self.vec_limit_deviation_angle_utility(true,source,cosineOfConeAngle,basis)
    
    
    @staticmethod
    def zero():
        return Vec2(0,0)

    @staticmethod
    def forward():
        return Vec2(0,1)

