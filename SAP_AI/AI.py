from tkinter import *
import pyautogui
import cv2 as cv
import numpy as np
import time
import valueRecogniton as VR
import itemrec as IR
from random import randint

lost = False

#add all the other animals
loclst = ["ant","ape","bever","bison","bull","cricket","deer","dolphine","doodoo","duck","fish","giraff","godfly","gorila","hog","horse","kangoroo","leopard","mosqito","parrot","phantasticGus","pufffish","rabbit","racoon","rat","rihno","scorpio","seaotter","shark","sheep","shrimp","snail","snake","spider","stink","untitledGoose","worm"]
cordlst = []
dub = False
hitman = []
name_cordinates_1 = [(375, 399),(942, 399),(1528, 399)]
name_cordinates_2 = [(375, 691),(942, 691),(1528, 691)]

class slot:
    def __init__(self,cor):
        self.cor = cor
        self.empty = True
        self.animal = None
        self.val = None
    
    def set(self,animal_posistion,animal_name,new_val):
        if self.empty == False:
            pyautogui.click(self.cor)
            pyautogui.click(1041, 983)
            time.sleep(2)
        pyautogui.click(animal_posistion)
        time.sleep(1)
        pyautogui.click(self.cor)
        self.animal = animal_name
        self.empty = False
        self.val = new_val




    

oldloc = (0,0)
slots = [slot((524,441)), slot((671, 441)),slot((818, 441)),slot((965, 441)),slot((1112, 441))]

# not in use yet
class Item:
    def __init__(self,cor,effect):
        self.effects = {'helth':'helth','attack':'attack','store':'store','spawn':'spawn','other': []}
        self.cor = cor
        self.effect = self.effects[effect]
        self.val = None
    
    def use(self,slot):
        pyautogui.click(self.cor)
        pyautogui.click(slot.cor)
        slot.val += self.val


class token:
    def __init__(self,name,attack,health,cordinates):
        self.name = name
        self.attack = attack
        self.health = health
        self.cordinates = cordinates
    def returnself(self):
        return [self.name,self.attack,self.health,self.cordinates]

main = Tk()

def check_if_empty(lst):
    shell = []
    if lst == [] or lst == None:
        shell.append([None,0,0,(0,0)])
        return shell
    else:
        return lst

def look_for_empty():
    for i in range(len(slots)):
        if slots[i].empty == True:
            return True

    return False

def drag_and_drop(upper : list,down: list):
    upper = check_if_empty(upper)
    down = check_if_empty(down)

    mid = upper[int(((len(upper) - 1) / 2) - 0.1)][2] + upper[int(((len(upper) - 1) / 2) - 0.1)][1]
    for i in range(len(down)):
        if down[i][1] + down[i][2] > mid or look_for_empty() == True:

            for x in range(len(slots)):
                if slots[x].empty == True:
                    slots[x].set((down[i][3][0] + 20,down[i][3][1] + 20),down[i][0],down[i][1] + down[i][2])
                    time.sleep(5)
                    break
                elif slots[x].val < down[i][1] + down[i][2] and look_for_empty() == False:
                    slots[x].set((down[i][3][0] + 20,down[i][3][1] + 20),down[i][0],down[i][1] + down[i][2])
                    time.sleep(5)
                    break
        else:
            continue

def id_tag(location):
    location = location + ".png"

    global oldloc,cordlst,dub
    
    ptlst = []

    img_rgb = cv.imread('src.png')
    print(location)

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(location,0)

    w, h = template.shape[::-1]

    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.60

    loc = np.where( res >= threshold)
    
    #get cordinates and draw rectangle
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
        ptlst.append(pt)
    
    ptlst = sorted(ptlst,key=lambda y : y[0])

    for i in range(len(ptlst)):
        if i == 0:
            values = VR.find(ptlst[i])
            cordlst.append(token(location,values[0],values[1],ptlst[i]))
            continue
        point = ptlst[i]
        opoint = ptlst[i - 1]
        print(opoint, point , point[0] - opoint[0])
        if point[0] - opoint[0] < 5:
            print(point[0] - opoint[0])
            continue
        else:
            
            cordlst.append(token(location,1,1,point))

    cv.imwrite('res.png',img_rgb)


def start():
    global lost,cordlst,dub,hitman

    starttxt = Label(main,text="starting in 5 seconds")
    starttxt.pack()
    time.sleep(5)
    starttxt.pack_forget()
    iterations = 0
    while lost == False:
        cordlst = []
        dub = False
        hitman = []

        scr = pyautogui.screenshot()
        scr.save("src.png")

        for loc in loclst:
            id_tag(loc)
        print(cordlst)

        tokenlst = []
        print(f"hitman : {hitman}")
        
        for i in range(int(len(cordlst))):
            print(cordlst[i])
            if cordlst[i].returnself() not in tokenlst:
                tokenlst.append(cordlst[i].returnself())

        upper = []
        down = []

        for token in tokenlst:
            current_token = token
            if current_token[3][1] > 555:
                down.append(current_token)
            else:
                upper.append(current_token)

        upper = sorted(upper,key=lambda x: x[1] + x[2])
        down = sorted(down,key=lambda x: x[3][0],)
        down = down[::-1]

        print("upper : {} down : {}".format(upper,down))

        drag_and_drop(upper,down)
        time.sleep(1)
        pyautogui.click(1536, 969)
        time.sleep(1)
        pyautogui.click(1238, 711)
        if iterations == 0:
            iterations = 1
            time.sleep(5)
            rand1 = randint(0,2)
            rand2 = randint(0,2)
            pyautogui.click(name_cordinates_1[rand1])
            time.sleep(0.1)
            pyautogui.click(name_cordinates_2[rand2])
            time.sleep(0.1)

            pyautogui.click(1697, 986)
        time.sleep(20)
        pyautogui.click(893, 428)
        time.sleep(3)
        pyautogui.click(893, 428)
        time.sleep(2)
    
    



b1 = Button(main,text="Begin",command=start)

b1.pack()
main.mainloop()
