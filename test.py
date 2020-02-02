import tellopy
import time
from tkinter import *

SPEED = 70
DELAY = 0.4

drone = tellopy.Tello()


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)

def tellotakeoff():
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        drone.connect()
        drone.wait_for_connection(60.0)
        drone.takeoff()
        time.sleep(1.1)
        drone.down(50)
        time.sleep(2)


def forwardD(x):
    drone.forward(SPEED)
    time.sleep(DELAY)
    drone.forward(0)

def backwardD(x):
    drone.backward(SPEED)
    time.sleep(DELAY)
    drone.backward(0)

def leftD(x):
    drone.left(SPEED)
    time.sleep(DELAY)
    drone.left(0)

def rightD(x):
    drone.right(SPEED)
    time.sleep(DELAY)
    drone.right(0)

def stopD(x):
    time.sleep(DELAY)
    drone.land()
    drone.quit()







# création d'une instance de la classe TK, que l'on affecte à l'objet "root"
tk = Tk()

# Quelques exemples de touches
tk.bind("<Up>", forwardD) # Flèche haut
tk.bind("<Down>", backwardD) # Bas
tk.bind("<Left>", leftD) # Gauche
tk.bind("<Right>", rightD) # Droite
tk.bind("<a>", stopD) # barre d'espace
tellotakeoff()
tk.mainloop()
