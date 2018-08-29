import os
import numpy as np
from face_recognition import load_image_file, face_encodings
import pickle



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

fifa_dict = {"names": known_face_names, "encode": known_face_encodings}

output = open('fifa_faces_endoded.pkl', 'wb')
pickle.dump(fifa_dict, output)
output.close()

print("End.")