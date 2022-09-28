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

def remove_sides(img):
    shape = (img.shape[0] + 5,img.shape[1] + 5)
    cv.rectangle(img,(0,0),shape,(0,0,0),35)

def initfy(cor):
    integer = []
    if type(cor) == str:
        for let in cor:
            if let.isnumeric():
                integer.append(let)
        try:
            return int("".join(integer))
        except:
            return None
    else:
        return cor


def find(cor):
    img = cv.imread('src.png')
    attack = img
    helth = img
    attack = img[cor[1] + 100:cor[1] + 180, cor[0] + -10:cor[0] + 80]
    helth = img[cor[1] + 100:cor[1] + 170, cor[0] + 70:cor[0] + 140]

    attack = applycolormask(attack,[0, 0, 150],[0, 250, 255])
    helth = applycolormask(helth,[0, 0, 150],[0, 250, 255])
    remove_sides(attack)
    remove_sides(helth)

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

    attackval = initfy(attackval)
    helthval = initfy(helthval)
    

    return (attackval,helthval)

print(find((753, 353)))
