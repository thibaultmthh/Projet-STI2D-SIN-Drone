import time
from math import sqrt, atan, degrees
import threading

import cv2

import tellopy

print("all loaded")


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
    def takeoff(*arg):
        print("takeoff")
    def land(*arg):
        print("land")

class Drone():
    def __init__(self):
        self.LIMIT_ALT = 2
        self.SDELAY = 1
        self.BDELAY = 20
        self.TESTING = True
        self.ECHELEVECTEUR = 0.06



        self.frame = None
        self.get_stream_thread = threading.Thread(target=self.get_stream)
        self.get_stream_thread.start()



        self.position = (0, 0)

        if self.TESTING:
            self.tello = fakeDrone()
        else:
            self.tello = tellopy.Tello()

        self.tello.connect()
        self.tello.wait_for_connection(60.0)
        self.tello.takeoff()
        self.tello.set_alt_limit(self.LIMIT_ALT)
        self.tello.up(50)
        time.sleep(6)
        self.tello.up(0)
        #self.tello.down(50)
        time.sleep(self.SDELAY)


    #------ Partie video ------#

    def get_stream(self):
        """Boucle infinie qui recupère les images de la camera du drone"""
        if self.TESTING:
            while True:
                cap = cv2.VideoCapture("data/salle1.mp4")

                while cap.isOpened:
                    time.sleep(0.02)
                    ret, frame = cap.read()
                    if ret:
                        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                        self.frame = gray

                    else:
                        break

    def get_frame(self):
        """return la derniere frame captée par la camera"""
        return self.frame


    # ----- Update des données internes ----

    def set_new_pos(self, pos):
        self.position = pos

    # ----Convertion des distance/angle en vitesse et temps de deplacement-----

    def distance_to_speed_nd_time(self, distance):
        """Prend comme parametre la distance en cm"""
        if distance > 8:
            speed = 60
            delay = (0.0177 * distance) + 0.256
        else:
            speed = 0
            delay = 0
        return (speed, delay)

    def angle_to_speed_nd_time(self, angle):
        """Prend comme parametre un angle en degrees"""
        if angle > 0.05:
            speed = 120
            delay = 0.0111 * angle
        else:
            speed = 0
            delay = 0
        return (speed, delay)

    # ----- Calcule de trajectoire interne -----
    def calcul_trajectoire(self, pos1, pos2):
        print("pos1, pos2", pos1, pos2)
        """return la distance et l'angle par rapport a l'axe y de l'a trajectoire la plus courte de 2 points"""
        vecteur = (pos2[0] - pos1[0], pos2[1] - pos1[1])  # xB - xA , yB-yA
        print("vecteur", vecteur)
        # a² + b² = c² pour trouver la norme avec pytagore sortie sans unitée
        normevecteur = sqrt(vecteur[0]**2 + vecteur[1]**2)
        # trigonometrie basique angle = artant(oposé/adjasant)
        if vecteur[0] != 0:
            angle = atan(vecteur[1] / vecteur[0])
            angle = degrees(angle)
        else:
            angle = 0

        angle, normevecteur = (angle, normevecteur /
                               self.ECHELEVECTEUR)  # Convertion en m
        print(angle)
        print(angle)
        if vecteur[0] > 0 and vecteur[1] >= 0:
            angle = 90-angle
            print("cas 1, angle = {}, vecteur = {}".format(angle,vecteur))
        elif vecteur[0] < 0 and vecteur[1] >= 0 :
            angle = -90-angle
            print("cas 2, angle = {}, vecteur = {}".format(angle,vecteur))

        elif vecteur[0] < 0 and vecteur[1] <=0:
            angle = -90-angle
            print("cas 3, angle = {}, vecteur = {}".format(angle,vecteur))

        elif vecteur[0] > 0 and vecteur[1] <=0:
            angle = 90-angle
            print("cas 4, angle = {}, vecteur = {}".format(angle,vecteur))

        if vecteur[0] == 0 and vecteur[1] < 0:
            angle = -180


        return normevecteur, angle

    # ---- Partie simplification des deplacement avancé

    def go_to(self, pos):
        pos1 = self.position
        pos2 = pos
        distance, angle = self.calcul_trajectoire(pos1, pos2)
        print('distance, angle', distance, angle)
        self.tourne(angle)
        time.sleep(0.3)
        self.avant(distance)
        time.sleep(self.SDELAY)
        self.tourne(-angle)
        time.sleep(0.3)
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
        time.sleep(0.1)


    def tourne_droite(self, angle):
        speed, delay = self.angle_to_speed_nd_time(angle)
        self.tello.clockwise(speed)
        time.sleep(delay)
        self.tello.clockwise(0)
        time.sleep(0.1)


    def avant(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        print("speed delay", speed, delay)
        self.tello.forward(speed)
        time.sleep(delay)
        self.tello.forward(0)
        time.sleep(self.SDELAY)


    def arriere(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.backward(speed)
        time.sleep(delay)
        self.tello.backward(0)
        time.sleep(self.SDELAY)


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
        time.sleep(self.SDELAY)


        # TODO: calibrage de la montée descente
    def haut(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.up(speed)
        time.sleep(delay)
        self.tello.up(0)
        time.sleep(self.SDELAY)


    def bas(self, distance):
        speed, delay = self.distance_to_speed_nd_time(distance)
        self.tello.down(speed)
        time.sleep(delay)
        self.tello.down(0)
        time.sleep(self.SDELAY)

    def landing(self):
        self.tello.land()



#########################################Partie perso################################################

def avancer(dist, pos, orientation):
    a = round(dist / quadrillage)
    print('se deplace de {} sur le tableau'.format(a))

    return pos


def donne_pos_tour(x):
    e = 2
    while x > 12:
        x -= 12
    if x ==1 or x == 4 or x == 7 or x == 10:
        a,b = (0,0)
    else:
        if x == 5 or x == 6 or x == 8:
            b = -e
        if x == 3 or x == 9:
            b = 0
        if x == 2 or x == 11 or x == 12:
            b  = e
        if x == 2 or x == 3 or x ==5:
            a = -e
        if x == 6 or x == 10 or x == 12:
            a = 0
        if x == 8 or x == 9 or x == 11:
            a = e
    return a,b


XSalle = 18 * 100
YSalle = 15 * 100
quadrillage = 0.1 * 100


XArray = round(XSalle / quadrillage)
YArray = round(YSalle / quadrillage)
posDrone = (0, 0)
orientationDrone = 0


drone = Drone()

while True:
    time.sleep(0.5)
    frame = drone.get_frame()
    cv2.imshow("test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)
