import numpy as np
from math import pi, sin, cos
from matplotlib import pyplot as plt
from random import random, randint, seed
from classes_meca import Vecteur3d as V3D

import pygame
import pygame.draw as pygDraw
from pygame.time import Clock as pygClock


class Kobuki(object):
    """Robot Mobile"""

    def __init__(self, rayon=0.075, distance=0.35, pos=V3D(), ori=0, nom='tortue', c='green'):

        self.pos = [pos]
        self.dist = distance    # dist entre les roues
        self.r = rayon  # rayon des roues
        self.vit_t = 0  # vitesse tout droit
        self.vit_r = 0
        self.ori = [ori]     # orientation

        a = self.r/2
        b = self.r/self.dist
        self.jacobian = np.array([[a, a], [b, -b]])

        self.nom = nom
        self.color = c

    def __str__(self):
        msg = 'Kobuki(' + str(self.pos[-1]) + ',' + ')'
        return msg

    def __repr__(self):
        msg = 'Kobuki(' + str(self.pos[-1]) + ',' + ')'
        return msg

    def mcd(self, vg=0, vd=0):
        vit_roues = np.array((vd, vg))
        vit_robot = np.dot(self.jacobian, vit_roues)

        return vit_robot

    def mci(self, vit_trans=0, vit_rot=0):
        vit_robot = np.array((vit_trans, vit_rot))
        vit_roues = np.dot(np.linalg.inv(self.jacobian), vit_robot)

        return vit_roues

    def simulMCD(self, dt, vg, vd):
        vit_rob = self.mcd(vg, vd)
        self.ori.append(self.ori[-1]+dt*vit_rob[1])

        dx = self.pos[-1].x+dt*vit_rob[0]*cos(self.ori[-1])
        dy = self.pos[-1].y+dt*vit_rob[0]*sin(self.ori[-1])
        self.pos.append(V3D(dx, dy))

    def simulMCI(self, dt, vt, vr):
        vit_roues = self.mci(vt, vr)
        vit_rob = np.array((vt, vr))
        self.ori.append(self.ori[-1]+dt*vit_rob[1])

        dx = self.pos[-1].x+dt*vit_rob[0]*cos(self.ori[-1])
        dy = self.pos[-1].y+dt*vit_rob[0]*sin(self.ori[-1])
        self.pos.append(V3D(dx, dy))

    def trajectoire(self):
        trajx = []
        trajy = []
        for i in range(0,len(self.pos)):
            trajx.append(self.pos[i].x)
            trajy.append(self.pos[i].y)
        plt.plot(trajx, trajy)  # color=self.color)
        plt.show()


class Simulateur(object):
    robots = []

    def __init__(self, nom):
        self.nom = nom

    def addKobuki(self, K=Kobuki()):
        self.robots.append(K)

    def removeKobuki(self, name):
        for r in self.robots:
            if r.nom == name:
                self.robots.remove(r)
            else:
                print('No Kobuki named ' + name + ' in simulateur ' + self.nom + '.')


    # def createNkobuki(self,n):
    #     for i in range (1,n):

    def trace(self):
        plt.figure('Plan de ' + self.nom)
        for t in self.robots:
            X = []
            Y = []
            for i in t.pos:
                X.append(i.x)
                Y.append(i.y)
            plt.plot(X, Y, color=t.color, label=t.nom)
            plt.legend()
        plt.show()

    def controlRoues(self, name, step, vg, vd):
        for r in self.robots:
            if r.nom == name:
                r.simulMCD(step, vg, vd)
            else:
                print('No Kobuki named ' + name + ' in simulateur ' + self.nom + '.')

    def trajSinMCD(self, step, duree, a=1, omega=1):
        """trajectoire de la forme A *sin(omega*t)"""
        t = [0]

        while t[-1] < duree:
            for r in self.robots:
                vg = a * abs(sin(omega * t[-1]))
                vd = a * abs(sin((pi/2*omega)+omega * t[-1]))
                r.simulMCD(step, vg, vd)
            t.append(t[-1]+step)

    def trajSinMCI(self,step, duree, a=pi/2, omega=1):
        t = [0]
        while t[-1] < duree:
            for r in self.robots:
                vr = a*sin(omega*t[-1])
                vt = 1
                r.simulMCI(step, vt, vr)
            t.append(t[-1]+step)

    def controlRouesRand(self, step, duree):
        t = [0]
        i=0
        while t[-1] < duree:
            i+=1
            t.append(t[-1] + step)
            for r in self.robots:
                seed(a=None, version=2)
                g = randint(-2, 5)
                d = randint(-2, 5)
                self.controlRoues(r.nom, step, g, d)

    # def goToPoint(self, name, x, y):
    #     for r in self.robots:
    #         if r.nom == name:
    #             dist_x = x - r.pos[-1].x
    #             dist_y = y - r.pos[-1].y
    #
    #             vg =
    #             vd =


#        return t



rob1 = Kobuki(nom='rob1', c='red')
rob2 = Kobuki(nom='rob2', c='blue')
rob3 = Kobuki(nom='rob3', c='green')
rob4 = Kobuki(nom='rob4', c='black')

simu = Simulateur('simu')
ehou2 = Simulateur('simu2')

simu.addKobuki(rob1)
#simu2.addKobuki(rob2)
dt = 0.01
time = 20

#simu.controlRouesRand(dt, time)
simu.trajSinMCI(dt,time)
simu.trace()


