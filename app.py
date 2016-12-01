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
        return Vec2(self.x*1.0/scalar, self.y*1.0/scalar)

    def mult(self, scalar):
        return Vec2(self.x*scalar, self.y*scalar)

    def lenght(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        lenght = self.lenght()
        if lenght > 0:
            return self.div(lenght)
        return self

    def cross(self):
        return Vec2(self.y, -self.x)

    def distance(self, v):
        return math.hypot(self.x-v.x, self.y-v.y)

    def parallel_component(self, unit_basis):
        projection = self.dot(unit_basis)
        return unit_basis.mult(projection)

    def truncate(self, max_length):
        length = self.lenght()        
        if (length > math.fabs(max_length)):
            return self.mult( max_length * 1.0 / length)
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

        return perp.lenght()

    def abs(self):
        return Vec2(self.x if self.x > 0 else -self.x, self.y if self.y > 0 else -self.y)

    def __repr__(self):
        return "(%d,%d)" % (self.x,self.y)

    def __str__(self):
        return "(%d,%d)" % (self.x,self.y)



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
        sourceLength = source.lenght()

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

    def __str__(self):
        return "Entity('%d','%s','%d','%d','%d','%d','%d',%d,%d,%d,%d)" % (
            self.entity_id, self.entity_type, self.position.x, self.position.y, self.velocity.x, self.velocity.y, self.state, self.radius, self.max_speed, self.mass, self.friction)
    def __repr__(self):
        return "Entity('%d','%s','%d','%d','%d','%d','%d',%d,%d,%d,%d)" % (
            self.entity_id, self.entity_type, self.position.x, self.position.y, self.velocity.x, self.velocity.y, self.state, self.radius, self.max_speed, self.mass, self.friction)

    def seek(self, me, vme, t, vt):
        
        max_velocity = vme.truncate(self.max_speed).lenght()

        future_t = t.add(vt.mult(3))

        desired_velocity = future_t.sub(me).normalize().mult(max_velocity)
        #steering = desired_velocity.sub(vi)   

        return (me.add(desired_velocity), desired_velocity, t.add(vt), vt)

    def get_steer_distance_to_unit(self, target):
        
        speed = self.steer_to_unit(target).lenght()

        return self.position.distance(target.position)/speed
        
    def steer_to(self, t, vt = None):
        if vt == None:
            vt = Vec2.zero()

        if (self.velocity.x ==0 and self.velocity.y ==0):
            return t

        max_velocity = 800
        
        future_t = t.add(vt.mult(2.0))
        desired_velocity = future_t.sub(self.position).normalize().mult(max_velocity)

        steering = desired_velocity.sub(self.velocity).normalize().mult(max_velocity)

        return self.position.add(steering)

    def steer_to_unit(self, target):        
        return self.steer_to(target.position, target.velocity)
        
        


class World:
    def __init__(self, my_team_raw):
        self.my_team_id = int(my_team_raw)
        self.spell = 0
        self.wizards = []
        self.snaffles = []
        self.opponents = []
        self.bludgers = []

    def add_spell(self):
        self.spell = self.spell + 1

    def make_spell(self):
        self.spell = self.spell - 20

    def __str__(self):
        s = "w = World(%d)" % self.my_team_id
        for el in self.wizards:
            s = s + "\nself.wizards.append(%s)" % el
        for el in self.snaffles:
            s = s + "\nself.snaffles.append(%s)" % el
        for el in self.opponents:
            s = s + "\nself.opponents.append(%s)" % el
        for el in self.bludgers:
            s = s + "\nself.bludgers.append(%s)" % el
        return s

    def read_raw_input(self):
        self.wizards = []
        self.snaffles = []
        self.opponents = []
        self.bludgers = []
        
        count_entities = int(raw_input())

        for i in xrange(count_entities):
            self.add_raw_input(raw_input())

 #       if debug:
 #           print >> sys.stderr, self

    def add_raw_input(self, raw):
#        if debug:
#            print >> sys.stderr, raw
        entity_id, entity_type, x, y, vx, vy, state = raw.split()
        if entity_type == "WIZARD":
            if debug:
                print >> sys.stderr, raw.split()
            self.wizards.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 400, 300, 1.0, 0.75))

        elif entity_type == "OPPONENT_WIZARD":
            self.opponents.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 400, 300, 1.0,0.75))

        elif entity_type == "SNAFFLE":
            self.snaffles.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 150, 800, 0.5, 0.9))

        elif entity_type == "BLUDGER":
            self.bludgers.append(Entity(entity_id, entity_type, x, y, vx, vy, state, 200, 600, 8.0, 0.75))


    def center(self):
        """ определяем центр игры"""
        return Vec2(8000, 3750)  # Entity("0 CENTER 8000 3750 0 0 0")

    def opponent_gate(self, wizard = None):
        """ определяем центр игры"""
        
        center = 3750
        if (wizard != None):
            center =  min(max(wizard.position.y, center - 800),3750 + 800)

        return Vec2(16000 if self.my_team_id == 0 else 0, center)

    def gate(self, wizard = None):
        """ определяем центр игры"""
        
        center = 3750
        if (wizard != None):
            center =  min(max(wizard.position.y, center - 800),3750 + 800)

        return Vec2(16000 if self.my_team_id == 1 else 0, center)


class Strategy:
    
    MOVE_SNAFFLE = 40
    MOVE_FORWARD = 45
    MOVE_BLUDGER = 50
    MOVE_FROM_BLUDGER = 60
    MOVE = 100

    THROW_SNAFFLE = 110
    THROW = 200

    CAST_OBLIVIATE  = 220
    CAST_PETRIFICUS = 230
    CAST_ACCIO      = 240
    CAST_FLIPENDO   = 250
    
    CAN_CAST_OBLIVIATE  = 1220
    CAN_CAST_PETRIFICUS = 1230
    CAN_CAST_ACCIO      = 1240
    CAN_CAST_FLIPENDO   = 1250


    HOLDING_SNAFFLE = 1100
    FIND_SNAFFLE = 1110
    FIND_SNAFFLE_ONE = 1115
    FIND_BLUDGER = 1120
    CAN_THROW = 1190

    PROBLEM_MOVE    = 1200
    PROBLEM_ONEBALL = 1210
    PROBLEM_ENEMY_AT_GATE = 1220
        
    def __init__(self,w):
        self.world = w
    
    def get_rules(self, wizard, prev_action):

        prev_snaffle = None if prev_action == None or prev_action[0] != Strategy.MOVE_SNAFFLE else prev_action[1] 
        near_snaffle = self.find_snaffle(wizard, prev_snaffle)
        near_bludger = self.find_bludger(wizard)
        accio        = self.find_accio_snaffle(wizard, prev_snaffle)
        flipendo     = self.find_flipendo_snaffle(wizard, prev_snaffle)


        check_throw = lambda w, snaffle: w > snaffle
        check_holding = lambda t : t.state == 1 
        not_none     = lambda t: t != None
        is_true      = lambda t: t == True


        #  Если мяч в руках, отобьем помечаю
        #  Если видим мяч, ты двигаемся к нему
        states = [
        (Strategy.PROBLEM_MOVE, Strategy.MOVE, None, None),
        (Strategy.PROBLEM_ONEBALL, Strategy.MOVE, None, None),
        (Strategy.MOVE, Strategy.CAN_CAST_FLIPENDO, not_none, [flipendo]),
        #(Strategy.MOVE, Strategy.CAN_CAST_ACCIO, not_none, [accio]),
        (Strategy.MOVE, Strategy.HOLDING_SNAFFLE, check_holding, [wizard]),
        (Strategy.MOVE, Strategy.FIND_BLUDGER, not_none, [near_bludger]),
        (Strategy.MOVE, Strategy.FIND_SNAFFLE, not_none, [near_snaffle]),
        (Strategy.MOVE, Strategy.FIND_SNAFFLE_ONE, is_true, [len(self.world.snaffles)==1]),
        (Strategy.MOVE, Strategy.MOVE_FORWARD, None, self.world.center()),
        (Strategy.FIND_BLUDGER, Strategy.MOVE_BLUDGER, None, near_bludger),
        (Strategy.FIND_SNAFFLE, Strategy.MOVE_SNAFFLE, None, near_snaffle),
        (Strategy.FIND_SNAFFLE_ONE, Strategy.MOVE_SNAFFLE, None, prev_snaffle),
        (Strategy.HOLDING_SNAFFLE, Strategy.THROW_SNAFFLE, None, self.world.opponent_gate(wizard)),
        (Strategy.CAN_CAST_ACCIO,Strategy.CAST_ACCIO,None, accio),
        (Strategy.CAN_CAST_FLIPENDO,Strategy.CAST_FLIPENDO,None, flipendo)
        ]

        return states

    def find_problem(self):
        """ ищу проблему которую пытаемся решить. По умолчанию это будет движение"""
        problem = Strategy.PROBLEM_MOVE
        if len(self.world.snaffles) == 1:        
            Strategy.PROBLEM_ONEBALL

        return problem

    def find_action(self, state, for_wizard, prev_action = None):
        """Определяем правило, которое работало по набору состояний"""
        prev_state = None
        current_rule = None

        rules = self.get_rules(for_wizard, prev_action)
        
        params = []

        while(state != prev_state):
            prev_state = state 

            filter_rules = filter(lambda x: x[0] == state and (x[2] == None or x[2](*x[3])), rules)

            for rule in filter_rules:
                state = rule[1]
                current_rule = rule
                break

        return current_rule[1], current_rule[3]


    def get_command(self, wizard, action):
        command = ""

        if isinstance(action[1],Vec2):
            obj = wizard.steer_to(action[1])
        else:
            obj = wizard.steer_to_unit(action[1])


        if action[0] <= Strategy.MOVE:
            command =  "MOVE %d %d %d %d" % (obj.x, obj.y, 150, action[0])

        elif action[0] <= Strategy.THROW:
            command = "THROW %d %d %d %d" % (obj.x, obj.y, 500, action[0])

        elif action[0] == Strategy.CAST_FLIPENDO:
            command = "FLIPENDO %d" % (action[1].entity_id)
            self.world.make_spell()

        elif action[0] == Strategy.CAST_ACCIO:
            command = "ACCIO %d" % (action[1].entity_id)
            self.world.make_spell()

        else:
            obj = self.world.center()
            command =  "MOVE %d %d %d" % (obj.x, obj.y, int(random.random()*50 + 100))
        
        return command
           

    def find_snaffle(self, for_wizard, prev_snaffle):
        """ ищем ближайший мяч для волшебника """
        near_snaffle = None
        min_dist = 100000
        for snaffle in self.world.snaffles:
            new_min = for_wizard.get_steer_distance_to_unit(snaffle)

            if (new_min < min_dist and (prev_snaffle == None or snaffle != prev_snaffle)):
                near_snaffle = snaffle
                min_dist = new_min

        return near_snaffle

        

    def find_accio_snaffle(self, for_wizard, prev_snaffle):
        """ ищем ближайший мяч для волшебника """

        if (self.world.spell < 20):
            return None

        gate = self.world.gate()

        min_dist = 10000

        accio = None
        for snaffle in self.world.snaffles:
            t = snaffle.position.add(snaffle.velocity)
            new_min = gate.distance(t)

            if new_min < min_dist and snaffle != prev_snaffle:
                accio = snaffle
                min_dist = new_min

        return accio

    def find_flipendo_snaffle(self, for_wizard, prev_snaffle):
        """ ищем ближайший мяч для волшебника """

        if (self.world.spell < 20):
            return None


        cur_pos = for_wizard.position.add(for_wizard.velocity)

        gate = self.world.opponent_gate()

        min_dist = 4000

        flipendo = None

        for snaffle in self.world.snaffles:
            t = snaffle.position.add(snaffle.velocity)

            if(gate.x > t.x > cur_pos.x or gate.x < t.x < cur_pos.x) :

                y = ((t.y - cur_pos.y) * 1.0/(t.x - cur_pos.x)) * (gate.x - t.x) + t.y


                dist = for_wizard.get_distance_to_unit(snaffle)

                # if new_min < min_dist and
                if (2300 < y < 5200) and snaffle != prev_snaffle and (600 < dist <  3000):
                    flipendo = snaffle
                    #min_dist = new_min
                    if debug:
                        print >> sys.stderr, "flippendo %s %d %s" % (for_wizard, y, snaffle)                

        return flipendo




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

        fw = w.wizards[0]
        sw = w.wizards[1]

        problem = s.find_problem()

        faction = s.find_action(problem, fw)
        saction = s.find_action(problem, sw)

        if faction[0] == saction[0] and faction[0] == Strategy.MOVE_SNAFFLE:
            if fw.get_distance_to_unit(faction[1]) > sw.get_distance_to_unit(saction[1]):
                faction = s.find_action(problem, fw, saction)
            else:
                saction = s.find_action(problem, sw, faction)
        elif faction[0] == Strategy.CAST_FLIPENDO:
                saction = s.find_action(problem, sw, faction)
        elif saction[0] == Strategy.CAST_FLIPENDO:
                faction = s.find_action(problem, fw, saction)
        elif faction[0] == Strategy.CAST_ACCIO:
                saction = s.find_action(problem, sw, faction)
        elif saction[0] == Strategy.CAST_ACCIO:
                faction = s.find_action(problem, fw, saction)

#        if debug:
#            print >> sys.stderr, w
#            print >> sys.stderr, fw
#            print >> sys.stderr, sw

        fcommand = s.get_command(fw,faction)
        scommand = s.get_command(sw,saction)

        w.add_spell()

        print fcommand
        print scommand
