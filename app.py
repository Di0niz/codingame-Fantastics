# -*- coding: utf-8 -*- 

import sys
import math

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

        entity_id, self.entity_type, x, y, vx, vy, state = rawinput.split()
        self.entity_id = int(entity_id)
        self.x = int(x)
        self.y = int(y)
        self.vx = int(vx)
        self.vy = int(vy)
        self.state = int(state)

    def is_wizard(self):
        return self.entity_type == "WIZARD"


class StategyProblem:
    """Описываем список задач, которые может решить стратегия"""
    THROW_SNAFFLE = 10

class StrategyState:
    CAN_THROW = 20
    FIND_SNAFFLE = 30
    MOVE_TO_SNAFFLE = 40
    THROW_SNAFFLE = 50



class World:
    def __init__(self, my_team_raw):
        self.my_team_id = int(my_team_raw)
        self.entities = []


    def read_raw_input(self):
        self.entities = []
        count_entities = int(raw_input())

        for i in xrange(count_entities):
            self.entities.append(Entity(raw_input()))
            
    def move(self):
        for wizard in filter(lambda x: x.is_wizard(), self.entities):
            
            # Edit this line to indicate the action for each wizard (0 <= thrust <= 150, 0 <= power <= 500)
            # i.e.: "MOVE x y thrust" or "THROW x y power"
            print "MOVE 8000 3750 100"


    def agent(self, wizard):
        
        near_snaffle = []

        check_throw = lambda wizard, snaffle: wizard > snaffle

        states = [
        (StrategyState.CAN_THROW,             StrategyState.THROW_SNAFFLE,      True,        check_throw, [near_snaffle]),

        ]   


    def find_problem(self):
        return StategyProblem.THROW_SNAFFLE

w = World(raw_input())

# game loop
while True:
    
    w.read_raw_input()
    w.move()



