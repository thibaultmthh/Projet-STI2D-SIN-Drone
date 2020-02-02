import cv2
import tellopy
import numpy as np
import time
import av
import numpy as np



def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        #print(data)
        pass


drone = tellopy.Tello()
drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

drone.connect()
drone.wait_for_connection(60.0)


print(drone.tello_addr)
STREAM_UDP_IP = "0.0.0.0"
STREAM_UDP_PORT = '11111'


a = 'udp://@'+STREAM_UDP_IP+":"+STREAM_UDP_PORT#+'?overrun_nonfatal=1&fifo_size=5000'
print(a)


cap = cv2.VideoCapture(a, cv2.CAP_PROP_FRAME_COUNT)

print("Z")
while (cap.isOpened()):
    print('E')
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

print("e d")
