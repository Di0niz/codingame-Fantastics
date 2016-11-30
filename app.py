# -*- coding: utf-8 -*- 

import sys
import math
import random

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

debug = False

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



class EntityState:
    """Описание состояния игрока"""
    HOLDING = 1
    OTHER = 0

class Entity:
    """Описание класса игрока"""

    def __init__(self, entity_id, entity_type, x, y, speed_x, speed_y, state, radius=100.0, max_speed = 150.0, mass=1.0, friction = 1.0):
        self.entity_id      = int(entity_id)
        self.entity_type    = entity_type
        self.position       = Vec2(int(x), int(y))
        self.velocity       = Vec2(int(speed_x),int(speed_y))
        self.state          = int(state)
        self.mass           = mass
        self.radius         = radius
        self.max_speed      = max_speed
        self.friction       = friction

    def get_distance_to_unit(self, unit):
        return self.position.distance(unit.position)


class StategyProblem:
    """Описываем список задач, которые может решить стратегия"""
    THROW_SNAFFLE = 10

class StrategyState:

    MOVE_SNAFFLE = 40
    MOVE_FORWARD = 45
    MOVE_BLUDGER = 50
    MOVE_FROM_BLUDGER = 60
    MOVE = 100

    THROW_SNAFFLE = 110
    THROW = 200

    HOLDING_SNAFFLE = 1100
    FIND_SNAFFLE = 1110
    FIND_SNAFFLE_ONE = 1115
    FIND_BLUDGER = 1120
    CAN_THROW = 1110


class World:
    def __init__(self, my_team_raw):
        self.my_team_id = int(my_team_raw)
        self.wizards = []
        self.snaffles = []
        self.opponents = []
        self.bludgers = []


    def read_raw_input(self):
        count_entities = int(raw_input())

        for i in xrange(count_entities):
            self.add_raw_input(raw_input())


    def add_raw_input(self, raw):
        entity_id, entity_type, x, y, vx, vy, state = raw.split()
        if entity_type == "WIZARD":
            self.wizards.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 400, 10**6, 1.0, 0.75))

        elif entity_type == "OPPONENT_WIZARD":
            self.opponents.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 400, 10**6, 1.0,0.75))

        elif entity_type == "SNAFFLE":
            self.snaffles.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 150, 10**6, 0.5, 0.9))

        elif entity_type == "BLUDGER":
            self.bludgers.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 200, 10**6, 8.0, 0.75))


    def center(self):
        """ определяем центр игры"""
        return Vec2(8000, 3750)  # Entity("0 CENTER 8000 3750 0 0 0")

    def opponent_gate(self, wizard):
        """ определяем центр игры"""

        return Vec2(16000 if self.my_team_id == 0 else 0, min(max(wizard.position.y, 3750 - 800),3750 + 800)) # Entity("0 GATE %d %d 0 0 0" % (16000 if self.my_team_id == 0 else 0, min(max(wizard.position.y, 3750 - 800),3750 + 800)))

class Strategy:
    def __init__(self,w):
        self.world = w
    
    def get_rules(self, wizard, prev_action):
        
        prev_snaffle = None if prev_action == None or prev_action[0] != StrategyState.MOVE_SNAFFLE else prev_action[1] 
        near_snaffle = self.find_snaffle(wizard, prev_snaffle)
        near_bludger = self.find_bludger(wizard)


        check_throw = lambda wizard, snaffle: wizard > snaffle
        check_holding = lambda w : w.state == 1 
        not_none     = lambda t: t != None
        is_true      = lambda t: t == True

        #  Если мяч в руках, отобьем помечаю
        #  Если видим мяч, ты двигаемся к нему
        states = [
        (StrategyState.MOVE, StrategyState.HOLDING_SNAFFLE, check_holding, [wizard]),
        (StrategyState.MOVE, StrategyState.FIND_BLUDGER, not_none, [near_bludger]),
        (StrategyState.MOVE, StrategyState.FIND_SNAFFLE, not_none, [near_snaffle]),
        (StrategyState.MOVE, StrategyState.FIND_SNAFFLE_ONE, is_true, [len(self.world.snaffles)==1]),
        (StrategyState.MOVE, StrategyState.MOVE_FORWARD, None, self.world.center()),
        (StrategyState.FIND_BLUDGER, StrategyState.MOVE_BLUDGER, None, near_bludger),
        (StrategyState.FIND_SNAFFLE, StrategyState.MOVE_SNAFFLE, None, near_snaffle),
        (StrategyState.FIND_SNAFFLE_ONE, StrategyState.MOVE_SNAFFLE, None, prev_snaffle),
        (StrategyState.HOLDING_SNAFFLE, StrategyState.THROW_SNAFFLE, None, self.world.opponent_gate(wizard), wizard),
        ]
        return states

    def find_action(self, state, for_wizard, prev_action = None):
        """Определяем правило, которое работало по набору состояний"""
        prev_state = None
        current_rule = None

        rules = self.get_rules(for_wizard, prev_action)
        params = []
        while(state != prev_state):

            for rule in rules:
                if (rule[0] == state):
                    # проверяем сработало правило или нет
                    if rule[2] == None or rule[2](*rule[3]):
                        state = rule[1]
                        current_rule = rule
                        
            prev_state = state 

        return current_rule[1], current_rule[3]


    def get_command(self, action):
        command = ""

        if type(action[1]) is Vec2:
            obj = action[1]
        else:
            obj = action[1].position


        if action[0] <= StrategyState.MOVE:
            command =  "MOVE %d %d %d" % (obj.x, obj.y, int(random.random()*50 + 100))

        elif action[0] <= StrategyState.THROW:
            command = "THROW %d %d %d" % (obj.x, obj.y, int(random.random()*200 + 300))

        else:
            obj = self.world.center()
            command =  "MOVE %d %d %d" % (obj.x, obj.y, int(random.random()*50 + 100))
        
        return command
           

    def find_snaffle(self, for_wizard, prev_snaffle):
        """ ищем ближайший мяч для волшебника """
        near_snaffle = None
        min_dist = 100000
        for snaffle in self.world.snaffles:
            new_min = for_wizard.get_distance_to_unit(snaffle)

            if (new_min < min_dist and (prev_snaffle == None or snaffle != prev_snaffle)):
                near_snaffle = snaffle
                min_dist = new_min

        return near_snaffle

    def find_bludger(self, for_wizard):
        """ ищем ближайший мяч для волшебника """
        near_object = None
        min_dist = 100000
        for snaffle in self.world.bludgers:
            new_min = for_wizard.get_distance_to_unit(snaffle)

            if (new_min < min_dist and new_min < 500):
                near_snaffle = snaffle
                min_dist = new_min

        return near_object


if __name__ == '__main__':
    debug = True
    
    w = World(raw_input())

    # game loop
    while True:

        w.read_raw_input()

        s = Strategy(w)

        wizards = w.wizards

        fw = wizards[0]
        sw = wizards[1]

        faction = s.find_action(StrategyState.MOVE, fw)
        saction = s.find_action(StrategyState.MOVE, sw)

        if faction[0] == saction[0] and faction[0] == StrategyState.MOVE_SNAFFLE:
            if fw.get_distance_to_unit(faction[1]) > fw.get_distance_to_unit(saction[1]):
                faction = s.find_action(StrategyState.MOVE, fw, saction)
            else:
                saction = s.find_action(StrategyState.MOVE, sw, faction)

        fcommand = s.get_command(faction)
        scommand = s.get_command(saction)

        print fcommand
        print scommand
