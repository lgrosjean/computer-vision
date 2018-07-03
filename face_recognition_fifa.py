import os
import numpy as np
# import matplotlib.pyplot as plt
from face_recognition import load_image_file, face_encodings, face_locations, compare_faces
from PIL import Image
import argparse
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Argument Parser
ap = argparse.ArgumentParser()
# ap.add_argument("-c", "--country", required=True,
#     help="country to examinate")
ap.add_argument("-s", "--save", required=True,
    help="name for saving")

args = vars(ap.parse_args())

save_name = args["save"]
# country = args["country"]

# Directory and path definition
CURRENT_FOLDER = os.getcwd()
print("cwd:", CURRENT_FOLDER)

SCRAPING_FOLDER = "scraping"
SCRAPING_PATH = os.path.join(CURRENT_FOLDER, SCRAPING_FOLDER)

PHOTOS_FOLDER = "photos"
PHOTOS_PATH = os.path.join(SCRAPING_PATH, PHOTOS_FOLDER)

TWITTER_FOLDER = "twitter"
TWITTER_PATH = os.path.join(SCRAPING_PATH, TWITTER_FOLDER)

TWITTER_PHOTOS_FOLDER = "photos"
TWITTER_PHOTOS_PATH = os.path.join(TWITTER_PATH, TWITTER_PHOTOS_FOLDER)

print("Starting.")

# Get list from photos twitter directory
file_list = os.listdir(TWITTER_PHOTOS_PATH)

# Intialize list of player found
player_list = list()

# Initialize dictionary where jey = player / value = photos found
photo_player_dict = {}

for file in file_list:

	FILE_PATH = os.path.join(TWITTER_PHOTOS_PATH, file)
	file_name, file_extension = os.path.splitext(file)
	
	if file_extension == ".jpg":

		player = file_name.split("_")[0]

		if player in player_list:
			photo_player_dict[player].append(FILE_PATH)
		else:
			player_list.append(player)
			photo_player_dict[player] = [FILE_PATH]

# Load images in face_recognition
player_load_dict = {}

for player in player_list:

	photo_list = photo_player_dict[player]
	player_load_dict[player] = []

	i = 1

	for photo in photo_list:

		photo_load = load_image_file(photo)
		player_load_dict[player].append(photo_load)

		print("{}: {} photo loaded!".format(player, i))
		i+=1

# Encode images in face_recognition
player_encoded_dict = {}

for player in player_list:

	photo_load_list = player_load_dict[player]
	player_encoded_dict[player] = []

	i = 1

	for photo_load in photo_load_list:

		try:
			photo_encoded = face_encodings(photo_load)[0]
			player_encoded_dict[player].append(photo_encoded)

			print("{} {} : photo encoded!".format(player, i))

		except IndexError:
			print("{} {}: No face detected.".format(player, i))

		i+=1

# Known face encoded and names
known_face_encodings = []
known_face_names = []

for player in player_list:

	photo_encoded_list = player_encoded_dict[player]

	for photo_encoded in photo_encoded_list:

		known_face_names.append(player)
		known_face_encodings.append(photo_encoded)


# Ask for photo to test
Tk().withdraw()
PHOTO_TEST_PATH = askopenfilename()
#os.system(PHOTO_TEST_PATH)
#img = Image.open(PHOTO_TEST_PATH)
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