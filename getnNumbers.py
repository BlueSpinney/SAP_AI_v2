from pydoc import Helper
import numpy as np
import cv2 as cv
from cv2 import imshow
from PIL import Image
from pytesseract import pytesseract


def get(im):
    #path to the tesseract executable
    pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(im ,config='--psm 6 digits')
    return text

def applycolormask(img,lower,upper):
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_red = np.array(lower)
    upper_red = np.array(upper)
 
    return cv.inRange(img, lower_red, upper_red)

def find(cor):
    img = cv.imread('src.png')
    attack = img
    helth = img
    attack = img[cor[1] + 120:cor[1] + 165, cor[0] + 10:cor[0] + 50]
    helth = img[cor[1] + 120:cor[1] + 165, cor[0] + 85:cor[0] + 117]

    attack = applycolormask(attack,[0, 0, 150],[0, 250, 255])
    helth = applycolormask(helth,[0, 0, 150],[0, 250, 255])

    cv.imwrite('attack.png',attack)
    cv.imwrite('helth.png',helth)
    attackval = get(attack)
    helthval = get(helth)
    try:
        attackval = int(attackval)
    except:
        attack = 1
    try:
        helthval = int(helthval)
    except:
        helthval = 1
    if helthval == '':
        helthval = 0
    if attackval == '':
        attackval = 0

    return (attackval,helthval)




