import tellopy
import time
from math import sqrt, atan, degrees


class fakeDrone():
    def __init__(self):
        pass

    def connect(*arg):
        print("Conected")

    def wait_for_connection(*arg):
        pass

    def set_alt_limit(*arg):
        print("limit fixed", arg[1:])

    def counter_clockwise(*arg):
        print("je tourne a gauche", arg[1:])

    def clockwise(*arg):
        print("je tourne a droite", arg[1:])

    def forward(*arg):
        print("je forward", arg[1:])

    def backward(*arg):
        print("je backward", arg[1:])

    def left(*arg):
        print("je left", arg[1:])

    def right(*arg):
        print("je right", arg[1:])

    def up(*arg):
        print("je up", arg[1:])

    def down(*arg):
        print("je down", arg[1:])


class Drone():
    def __init__(self):
        self.LIMIT_ALT = 2
        self.SDELAY = 1
        self.BDELAY = 20
        self.TESTING = True
        self.ECHELEVECTEUR = 0.1

        self.position = (0, 0)

        if self.TESTING:
            self.tello = fakeDrone()
        else:
            self.tello = tellopy.Tello()

        self.tello.connect()
        self.tello.wait_for_connection(60.0)

        self.tello.set_alt_limit(self.LIMIT_ALT)

    # ----- Update des données internes ----

    def set_new_pos(self, pos):
        self.position = pos

    # ----Convertion des distance/angle en vitesse et temps de deplacement-----

    def distance_to_speed_nd_time(self, distance):
        speed = 60
        delay = (0.0177 * distance) + 0.256
        return (speed, delay)

    def angle_to_speed_nd_time(self, angle):
        speed = 120
        delay = 0.0111 * angle
        return (speed, delay)

    # ----- Calcule de trajectoire interne -----
    def calcul_trajectoire(self, pos1, pos2):
        """return la distance et l'angle par rapport a l'axe y de l'a trajectoire la plus courte de 2 points"""
        vecteur = (pos2[0] - pos1[0], pos2[1] - pos1[1])  # xB - xA , yB-yA
        # a² + b² = c² pour trouver la norme avec pytagore sortie sans unitée
        normevecteur = sqrt(vecteur[0]**2 + vecteur[1]**2)
        # trigonometrie basique angle = artant(oposé/adjasant)
        angle = atan(vecteur[1] / vecteur[0])
        angle = degrees(angle)
        angle = 90 - angle  # angle par rappor a l'axe y
        angle, normevecteur = (angle, normevecteur /
                               self.ECHELEVECTEUR)  # Convertion en m
        return normevecteur, angle

    # ---- Partie simplification des deplacement avancé

    def go_to(self, pos):
        pos1 = self.position
        pos2 = pos
        distance, angle = self.calcul_trajectoire(pos1, pos2)
        self.tourne(angle)
        self.avant(distance)
        self.tourne(-angle)
        return pos2

    def tourne(self, angle):
        if angle == 0:
            pass
        elif angle > 0:
            self.tourne_droite(angle)
        elif angle < 0:
            self.tourne_gauche(-angle)

    # ---- Partie simplification des deplacement basic -----
    def tourne_gauche(self, angle):
        speed, delay = self.angle_to_speed_nd_time(angle)
        self.tello.counter_clockwise(speed)
        time.sleep(delay)
        self.tello.counter_clockwise(0)

    def tourne_droite(self, angle):
        speed, delay = self.angle_to_speed_nd_time(angle)
        self.tello.clockwise(speed)
        time.sleep(delay)
        self.tello.clockwise(0)

    def avant(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.forward(speed)
        time.sleep(delay)
        self.tello.forward(0)

    def arriere(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.backward(speed)
        time.sleep(delay)
        self.tello.backward(0)

    def droite(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.right(speed)
        time.sleep(delay)
        self.tello.right(0)

    def gauche(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.left(speed)
        time.sleep(delay)
        self.tello.left(0)

        # TODO: calibrage de la montée descente
    def haut(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.up(speed)
        time.sleep(delay)
        self.tello.up(0)

    def bas(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.down(speed)
        time.sleep(delay)
        self.tello.down(0)


#########################################Partie perso################################################

def avancer(dist, pos, orientation):
    a = round(dist / quadrillage)
    print('se deplace de {} sur le tableau'.format(a))

    return pos


"""
def calcul_trajectoire(pos1,pos2):
    #"return la distance et l'angle par rapport a l'axe y de l'a trajectoire la plus courte de 2 points"

    vecteur = (pos2[0]-pos1[0],pos2[1]-pos1[1]) #xB - xA , yB-yA
    normevecteur = sqrt(vecteur[0]**2 + vecteur[1]**2) #a² + b² = c² pour trouver la norme avec pytagore sortie sans unitée
    x = atan(vecteur[1]/vecteur[0]) # trigonometrie basique angle = artant(oposé/adjasant)
    x = degrees(x)
    x = 90-x # angle par rappor a l'axe y
    return normevecteur , x
"""

def donne_pos_tour(x):
    while x > 12:
        x -= 12
    if x ==1 or x == 4 or x == 7 or x == 10:
        a,b = (0,0)
    else:
        if x == 5 or x == 6 or x == 8:
            b = -8
        if x == 3 or x == 9:
            b = 0
        if x == 2 or x == 11 or x == 12:
            b  = 8
        if x == 2 or x == 3 or x ==5:
            a = -8
        if x == 6 or x == 10 or x == 12:
            a = 0
        if x == 8 or x == 9 or x == 11:
            a = 8
    return a,b


XSalle = 18 * 100
YSalle = 15 * 100
quadrillage = 0.1 * 100


XArray = round(XSalle / quadrillage)
YArray = round(YSalle / quadrillage)
posDrone = (0, 0)
orientationDrone = 0


drone = Drone()
dir = (5, 6)

a = 0
b = 0
c = a, b
print(donne_pos_tour(2))
print(donne_pos_tour(657609590))
