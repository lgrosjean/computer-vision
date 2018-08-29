import pickle
import argparse
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import numpy as np
from face_recognition import face_encodings, face_locations, compare_faces

# Argument Parser
ap = argparse.ArgumentParser()
# ap.add_argument("-c", "--country", required=True,
#     help="country to examinate")
ap.add_argument("-s", "--save", required=True,
    help="name for saving")

args = vars(ap.parse_args())

save_name = args["save"]

# Read photo already encoded
pkl_file = open('fifa_faces_endoded.pkl', 'rb')
fifa_dict = pickle.load(pkl_file)
pkl_file.close()

known_face_names = fifa_dict["names"]
known_face_encodings = fifa_dict["encode"]
#fifa_dict = {"names": known_face_names, "encode": known_face_encodings}

print("Encoded photos loaded !")

# Ask for photo to test
Tk().withdraw()
PHOTO_TEST_PATH = askopenfilename()

file_name, file_extension = os.path.splitext(PHOTO_TEST_PATH)

print(file_extension)

if file_extension in [".MP4", ".mp4"]:

    cap = cv2.VideoCapture(PHOTO_TEST_PATH)

    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    i = 0

    # Read until video is completed
    while(cap.isOpened()):


        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret == True:

            print("Encoding starts.")

            # Display the resulting frame
            small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
            rgb_small_frame = small_frame[:, :, ::-1]


            # Faces found locations 
            face_found_locations = face_locations(rgb_small_frame)

            #print("Number of faces found:", len(face_found_locations))

            # Face found encoding
            face_found_encoded_list = face_encodings(rgb_small_frame, face_found_locations)

            # Matching faces in picture
            face_names = []
            for face_found_encoded in face_found_encoded_list:
                
                # See if the face is a match for the known face(s)
                matches = compare_faces(known_face_encodings, face_found_encoded)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

            # Add box and names for each faces found
            for (top, right, bottom, left), name in zip(face_found_locations, face_names):

                  # Draw a box around the face
                  cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                  # Add the name below the face
                  font = cv2.FONT_HERSHEY_DUPLEX
                  cv2.putText(frame, name, (left + 5, bottom - 5), font, 0.5, (255, 255, 255), 1)

            i+=1

            print("{}/{} frame treated.".format(i, frames))

            out.write(frame)
            cv2.imshow('Smile Detector', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else: 
            break

    print("ok")
    cap.release()
    out.release()
    cv2.destroyAllWindows()


else:

    img = cv2.imread(PHOTO_TEST_PATH)
    frame = np.asarray(img)
    small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
    rgb_small_frame = small_frame[:, :, ::-1]


    # Faces found locations 
    face_found_locations = face_locations(rgb_small_frame)

    print("Number of faces found:", len(face_found_locations))

    # Face found encoding
    face_found_encoded_list = face_encodings(rgb_small_frame, face_found_locations)

    # Matching faces in picture
    face_names = []
    for face_found_encoded in face_found_encoded_list:
        
        # See if the face is a match for the known face(s)
        matches = compare_faces(known_face_encodings, face_found_encoded)
        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    # Add box and names for each faces found
    for (top, right, bottom, left), name in zip(face_found_locations, face_names):

          # Draw a box around the face
          cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

          # Add the name below the face
          font = cv2.FONT_HERSHEY_DUPLEX
          cv2.putText(frame, name, (left + 5, bottom - 5), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image

    displayOK = True

    while displayOK:
        cv2.imshow('Faces located', frame)
        c = cv2.waitKey(-1) 
        if c >= 0:
            displayOK = False

    img_name = save_name + ".jpg"

    cv2.imwrite(img_name, frame);

    print("Photo saved!")