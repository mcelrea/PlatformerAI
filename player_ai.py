import pygame
import random
import time
from player import *

class PlayerAI:

    def __init__(self):
        self.player = Player()
        self.dna = []
        self.create_dna_sequence()
        self.currentAllele = 0
        self.delay = 1_000_000_000
        self.next_act = time.time_ns() + self.delay

    def create_dna_sequence(self):
        # 0 - junk DNA - 80%
        # 1 - jump - 6%
        # 2 - move left - 7%
        # 3 - move right - 7%

        for i in range(100):
            choice = random.randint(1,100)
            if(choice <= 50): #junk
                self.dna.append(0)
            elif(choice <= 86): #jump
                self.dna.append(1)
            elif(choice <= 93): #move left
                self.dna.append(2)
            elif(choice <= 100): #move right
                self.dna.append(3)

    def act(self):
        #print(str(time.time_ns()))
        if self.next_act < time.time_ns():
            if self.dna[self.currentAllele] == 1:
                self.player.jump()
            elif self.dna[self.currentAllele] == 2:
                self.player.move_left()
            elif self.dna[self.currentAllele] == 3:
                self.player.move_right()
            self.next_act = time.time_ns() + self.delay
            self.currentAllele += 1
            print(str(self.currentAllele) + ":" + str(self.dna[self.currentAllele]))

        return self.player.act()

    def draw(self, screen):
        self.player.draw(screen)

    def setMap(self, map):
        self.player.setMap(map)

    def get_score(self):
        return self.player.get_score()