import tellopy
import time

def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)
        pass
SPEED = 120
TIME = 4

def decolage():
    drone.takeoff()
    time.sleep(1.5)
    drone.down(50)
    time.sleep(4)
    drone.down(0)


def stop():
    time.sleep(2.2)
    drone.land()
    drone.quit()


def avancer(SPEED,TIME):
    drone.forward(SPEED)
    time.sleep(TIME)
    drone.forward(0)


def rotation(SPEED,TIME):
    drone.counter_clockwise(SPEED)
    time.sleep(TIME)
    drone.counter_clockwise(0)


drone = tellopy.Tello()
drone.connect()
drone.wait_for_connection(60.0)
drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

drone.set_alt_limit(0.8)


decolage()
drone.up(50)
time.sleep(10)
drone.up(0)
stop()
