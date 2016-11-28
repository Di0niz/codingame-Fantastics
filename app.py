# -*- coding: utf-8 -*- 

import sys
import math
import random

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

class EntityState:
    """Описание состояния игрока"""
    HOLDING = 1
    OTHER = 0

class Entity:
    """Описание класса игрока"""

    def __init__(self, rawinput):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
#        print >> sys.stderr, rawinput
        entity_id, self.entity_type, x, y, vx, vy, state = rawinput.split()
        self.entity_id = int(entity_id)
        self.x = int(x)
        self.y = int(y)
        self.vx = int(vx)
        self.vy = int(vy)
        self.state = int(state)

    def is_wizard(self):
        return self.entity_type == "WIZARD"
    def is_snaffle(self):
        return self.entity_type == "SNAFFLE"

    def is_bludger(self):
        return self.entity_type == "BLUDGER"

    def get_distance_to(self, x, y):
        return math.hypot(x - self.x, y - self.y)

    def get_distance_to_unit(self, unit):
        return self.get_distance_to(unit.x, unit.y)


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
        self.entities = []


    def read_raw_input(self):
        self.entities = []
        count_entities = int(raw_input())

        for i in xrange(count_entities):
            self.entities.append(Entity(raw_input()))

    def wizards(self):
        return filter(lambda x: x.is_wizard(), self.entities)
        
    def snaffles(self):
        return filter(lambda x: x.is_snaffle(), self.entities)

    def bludgers(self):
        return filter(lambda x: x.is_bludger(), self.entities)

    def center(self):
        """ определяем центр игры"""
        return Entity("0 CENTER 8000 3750 0 0 0")

    def opponent_gate(self, wizard):
        """ определяем центр игры"""

        return Entity("0 GATE %d %d 0 0 0" % (16000 if self.my_team_id == 0 else 0, min(max(wizard.y,3750 - 1800),3750 + 1800)))

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

        #  Если мяч в руках, отобьем помечаю
        #  Если видим мяч, ты двигаемся к нему
        states = [
        (StrategyState.MOVE, StrategyState.HOLDING_SNAFFLE, check_holding, [wizard]),
        (StrategyState.MOVE, StrategyState.FIND_BLUDGER, not_none, [near_bludger]),
        (StrategyState.MOVE, StrategyState.FIND_SNAFFLE, not_none, [near_snaffle]),
        (StrategyState.MOVE, StrategyState.FIND_SNAFFLE_ONE, not_none, [prev_snaffle]),
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
        if action[0] <= StrategyState.MOVE:
            obj = action[1]
            command =  "MOVE %d %d %d" % (obj.x, obj.y, int(random.random()*50 + 100))

        elif action[0] <= StrategyState.THROW:
            obj = action[1] 
            command = "THROW %d %d %d" % (obj.x, obj.y, int(random.random()*200 + 300))

        else:
            obj = self.world.center()
            command =  "MOVE %d %d %d" % (obj.x, obj.y, int(random.random()*50 + 100))
        
        return command
           

    def find_snaffle(self, for_wizard, prev_snaffle):
        """ ищем ближайший мяч для волшебника """
        near_snaffle = None
        min_dist = 100000
        for snaffle in self.world.snaffles():
            new_min = for_wizard.get_distance_to_unit(snaffle)

            if (new_min < min_dist and (prev_snaffle == None or snaffle != prev_snaffle)):
                near_snaffle = snaffle
                min_dist = new_min

        return near_snaffle

    def find_bludger(self, for_wizard):
        """ ищем ближайший мяч для волшебника """
        near_object = None
        min_dist = 100000
        for snaffle in self.world.bludgers():
            new_min = for_wizard.get_distance_to_unit(snaffle)

            if (new_min < min_dist and new_min < 500):
                near_snaffle = snaffle
                min_dist = new_min

        return near_object


if __name__ == '__main__':
    w = World(raw_input())

    # game loop
    while True:

        w.read_raw_input()
        #w.move()

        s = Strategy(w)

        wizards = w.wizards()

        actions = {}

        fw = wizards[0]
        sw = wizards[1]

        faction = s.find_action(StrategyState.MOVE, fw)
        saction = s.find_action(StrategyState.MOVE, sw)

        if faction[0] == saction[0] and faction[0] == StrategyState.MOVE_SNAFFLE:
            if fw.get_distance_to_unit(faction[1]) > fw.get_distance_to_unit(saction[1]):
                fw,sw = sw,fw
                faction = saction

        saction = s.find_action(StrategyState.MOVE, sw, faction)

        fcommand = s.get_command(faction)
        scommand = s.get_command(saction)

        print fcommand
        print scommand


