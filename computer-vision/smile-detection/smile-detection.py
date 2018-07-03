import cv2
import numpy as np
import sys
import argparse

parser = argparse.ArgumentParser(description=
    "How to use : \
    python smile-dection.py : run simply the code  |  \
    python smile-detection.py 'NAME_OF_FILE' : allows you to save \
    the video with the name NAME_OF_FILE.avi"
    )

args = parser.parse_args()

arg_list = sys.argv

capt_bool = (len(arg_list) > 1)

if capt_bool: 
    video_name = arg_list[1] + ".avi"

facePath = "haarcascade_frontalface_default.xml"
smilePath = "haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

if capt_bool:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_name,fourcc, 20.0, (640,480))

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
        x_face, y_face = (x, y)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.2,
            minNeighbors=22,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
            )

        # Set region of interest for smiles
        for (x, y, w, h) in smile:
            print("Found", len(smile), "smiles!")
            cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)
            cv2.putText(frame, 
                "Smiling!", 
                (x_face,y_face), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

    #cv2.cv.Flip(frame, None, 1)
    if capt_bool:
        out.write(frame)

    cv2.imshow('Smile Detector', frame)
    c = cv2.waitKey(7) % 0x100
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
