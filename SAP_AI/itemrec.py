from shutil import ExecError
import cv2 as cv
import numpy as np

items = [['apple',' + 2'],['chilli',' + 5'],['choclate','+ 4'],['garlac','* 1.5'],['honey',' + 3'],['meat','+ 4']]
cordinate_list = {}

def get_current_items(img_name,i):


    merge_img = cv.imread("C:\\Users\\Jerome\\OneDrive\\Desktop\\SAP_AI\\items\\" + img_name,0)
    loc = None

    current_sorce = cv.imread('src.png')
    current_sorce = current_sorce[600:800,1000:1800]
    img_rgb = cv.imread('src.png')

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    w, h = merge_img.shape[::-1]

    res = cv.matchTemplate(img_gray,merge_img,cv.TM_CCOEFF_NORMED)
    threshold = 0.50

    loc = np.where( res >= threshold)

    # Make functional for multiple items of the same type
    for pt in zip(*loc[::-1]):
        cordinate_list[img_name[0:len(img_name) - 4]] = [items[i][1]]
        cordinate_list[img_name[0:len(img_name) - 4]].append(pt)

    
def main():
    global raw_corlst
    raw_corlst = []
    for i in range(len(items)):
        parameter_for_item_gathering = items[i][0] + ".png"
        print('\n')
        get_current_items(parameter_for_item_gathering,i)
    return cordinate_list


