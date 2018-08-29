import cv2
import numpy as np
import sys

facePath = "haarcascade_frontalface_default.xml"
smilePath = "haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)



fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

sF = 1.05

while True:

    ret, frame = cap.read() # Capture frame-by-frame
    img = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor= sF,
        minNeighbors=8,
        minSize=(55, 55),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # ---- Draw a rectangle around the faces

    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) # all face
        # cv2.circle(frame, (x+w//2, y+h//2), 5, (0, 0, 255), -1) # center of face
        # # cv2.circle(frame, (x+w//2, y+h), 5, (0, 0, 255), -1) # center of face


        # dst = cv2.cornerHarris(gray,2,3,0.04)
        
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        edges = cv2.Canny(fgmask,200,255)

        # roi_gray = gray[y:y+h, x:x+w]
        # roi_color = frame[y:y+h, x:x+w]

        frame[dst>0.01*dst.max()]=[0,0,255]


        # smile = smileCascade.detectMultiScale(
        #     roi_gray,
        #     scaleFactor= 1.7,
        #     minNeighbors=22,
        #     minSize=(25, 25),
        #     flags=cv2.CASCADE_SCALE_IMAGE
        #     )

        # # Set region of interest for smiles
        # for (x, y, w, h) in smile:
        #     print("Found", len(smile), "smiles!")
        #     cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)
        #     #print "!!!!!!!!!!!!!!!!!"

    #cv2.cv.Flip(frame, None, 1)
    # out.write(frame)
    # cv2.imshow('Smile Detector', frame)
    cv2.imshow('Smile', edges)
    #cv2.imshow('frame',fgmask)
    c = cv2.waitKey(7) % 0x100
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
