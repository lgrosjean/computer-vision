import os
import subprocess
import shutil  # Move file from source to destination

nations = [
    "russia",
    "saudi-arabia",
    "egypt",
    "uruguay",
    "portugal",
    "spain",
    "morocco",
    "iran",
    "france",
    "australia",
    "peru",
    "denmark",
    "argentina",
    "iceland",
    "croatia",
    "nigeria",
    "brazil",
    "switzerland",
    "costa-rica",
    "serbia",
    "germany",
    "mexico",
    "sweden",
    "korea-republic",
    "belgium",
    "panama",
    "tunisia",
    "england",
    "poland",
    "senegal",
    "colombia",
    "japan"
    ]

CURRENT_FOLDER = os.getcwd()
PHOTOS_FOLDER = "photos"
PHOTOS_PATH = os.path.join(CURRENT_FOLDER, PHOTOS_FOLDER)

files = os.listdir(PHOTOS_PATH)

print("{} photos found".format(len(files)))

for nation in nations:

    NATION_PATH = os.path.join(PHOTOS_PATH, nation)

    if not os.path.exists(NATION_PATH):
        os.makedirs(NATION_PATH)

i=1

for file in files:

    FILE_PATH = os.path.join(PHOTOS_PATH, file)
    isFile = os.path.isfile(FILE_PATH)

    if isFile:

        country_found = False

        for nation in nations:

            NATION_PATH = os.path.join(PHOTOS_PATH, nation)

            if nation in file: 

                country_found = True

                shutil.copy2(FILE_PATH, NATION_PATH) 

                print("{} photos treated".format(i))
                i+=1

        if country_found:
            os.remove(FILE_PATH)

print("Finish.")

open_explorer = 'explorer ' + PHOTOS_PATH
subprocess.Popen(open_explorer)

