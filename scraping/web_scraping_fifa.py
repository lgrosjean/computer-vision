import os
from time import sleep
import argparse
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import subprocess
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--number", required=True,
    help="number of picture to scrap")

args = vars(ap.parse_args())

n = int(args["number"])



CURRENT_FOLDER = os.getcwd()
PHOTOS_FOLDER = "photos"
PHOTOS_PATH = os.path.join(CURRENT_FOLDER, PHOTOS_FOLDER)

if not os.path.exists(PHOTOS_PATH):
    os.makedirs(PHOTOS_PATH)

url = "http://fr.fifa.com/worldcup/photos/all-photos"

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
response = opener.open(url)

path_to_web_driver = "./chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(
    executable_path=path_to_web_driver,
    chrome_options=options)

browser.get(url)

photos_per_page = 24

number_of_click = n // photos_per_page 
clickAgain = (number_of_click > 0)


while clickAgain:

    print(number_of_click)

    element = browser.find_element_by_class_name("fi-btn") 
    browser.execute_script("arguments[0].click();", element)
    print("One click !")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    print("Scroll down!")
    number_of_click -= 1

    sleep(5)

    if number_of_click == 0:

        clickAgain = False

sleep(10)

html = browser.page_source
soup = BeautifulSoup(html, "lxml")

picture_boxes = soup.find_all("div", class_="col-xs-12 col-sm-4 col-md-3 col-flex")

print("Length", len(picture_boxes))

ii = 1

for i in range(n):

    picture_box = picture_boxes[i]
    
    name = picture_box["data-slug"]
    print(name)

    picture = picture_box.find("a")
    picture_url = picture["data-src"]

    print(picture_url)

    PICTURE_NAME = name + ".jpg"
    PICTURE_PATH = os.path.join(PHOTOS_FOLDER, PICTURE_NAME)

    webpage = opener.open(picture_url)

    if not os.path.isfile(PICTURE_PATH):

        f = open(PICTURE_PATH, "wb")
        content = webpage.read()
        f.write(content)
        f.close()

        ii +=1

print("{} new photos found !".format(ii-1))


open_explorer = 'explorer ' + PHOTOS_PATH
subprocess.Popen(open_explorer)

