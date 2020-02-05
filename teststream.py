import cv2
import time
print("cv2 loaded")


detector = cv2.CascadeClassifier('detectors/1.xml')

while True:
    cap = cv2.VideoCapture("data/2.mp4")
    #cap = cv2.VideoCapture(0)
    while cap.isOpened:
        time.sleep(0.001)
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray,(300,300))
            body = detector.detectMultiScale(gray, 1.04, 2)
            for (x,y,w,h) in body:
                cv2.rectangle(gray, (x,y), (x+w,y+h), (255,0,0), 3)


            cv2.imshow("win", gray)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit(0)

        else:
            break
    cap.release()
cv2.destroyAllWindows()
