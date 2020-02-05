import cv2
import time
print("cv2 loaded")


detector = cv2.CascadeClassifier('detectors/face1.xml')
detector2 = cv2.CascadeClassifier("detectors/profilface.xml")
detector3 = cv2.CascadeClassifier("detectors/1.xml")
a = 0
while True:
    cap = cv2.VideoCapture("data/salle2.mp4")
    #cap = cv2.VideoCapture(0)
    while cap.isOpened:
        a +=1
        time.sleep(0.001)
        ret, frame = cap.read()
        print(a)
        if ret :
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #gray = cv2.resize(gray,(300,300))
            body = detector.detectMultiScale(frame, 3, 5)
            #body2 = detector2.detectMultiScale(frame, 1.7, 5)
            body3 = detector3.detectMultiScale(frame, 1.06,5)
            for (x,y,w,h) in body:
                cv2.rectangle(gray, (x,y), (x+w,y+h), (255,0,0), 3)
            """
            for (x,y,w,h) in body2:
                cv2.rectangle(gray, (x,y), (x+w,y+h), (255,0,0), 3)
            """
            for (x,y,w,h) in body3:
                cv2.rectangle(gray, (x,y), (x+w,y+h), (0,255,0), 3)


            cv2.imshow("win", gray)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                exit(0)

        else:
            break
    cap.release()
cv2.destroyAllWindows()
