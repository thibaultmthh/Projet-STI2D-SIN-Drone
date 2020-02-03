import tello
import time

drone = tello.Tello('', 8889)
drone.takeoff()
time.sleep(5)

drone.move_forward(2)
time.sleep(6)
drone.move_backward(2)
time.sleep(6)

print(drone.land())
