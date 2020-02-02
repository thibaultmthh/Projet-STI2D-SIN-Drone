import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
import threading
from tkinter import *
class stream(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        try:
            retry = 3
            container = None
            while container is None and 0 < retry:
                retry -= 1
                try:
                    container = av.open(drone.get_video_stream())
                except av.AVError as ave:
                    print(ave)
                    print('retry...')

            # skip first 300 frames
            frame_skip = 300
            while True:
                for frame in container.decode(video=0):
                    if 0 < frame_skip:
                        frame_skip = frame_skip - 1
                        continue
                    start_time = time.time()
                    image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    cv2.imshow('Original', image)
                    cv2.waitKey(1)
                    if frame.time_base < 1.0/60:
                        time_base = 1.0/60
                    else:
                        time_base = frame.time_base
                    frame_skip = int((time.time() - start_time)/time_base)


        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print(ex)
        finally:
            drone.quit()
            cv2.destroyAllWindows()


SPEED = 200
DELAY = 0.05



def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)

def tellotakeoff():

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

class control(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
    # création d'une instance de la classe TK, que l'on affecte à l'objet "root"
        tk = Tk()

        # Quelques exemples de touches
        tk.bind("<Up>", forwardD) # Flèche haut
        tk.bind("<Down>", backwardD) # Bas
        tk.bind("<Left>", leftD) # Gauche
        tk.bind("<Right>", rightD) # Droite
        tk.bind("<a>", stopD) # barre d'espace
        tk.mainloop()
drone = tellopy.Tello()
drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
drone.connect()
drone.wait_for_connection(60.0)
b = control()
b.start()

#a = stream()
#a.start()

time.sleep(1)
tellotakeoff()
