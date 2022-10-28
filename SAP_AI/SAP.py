#Super Auto Pets AI work in Progress pre Alpha Version (with partial item recognition) v3.3
#TO-DO
#Optimize animal recognition
#add full Item usage

from tkinter import *
import pyautogui
import cv2 as cv
import numpy as np
import time
import valueRecogniton as VR
import itemrec as IR
from random import randint, randrange
import toolkit as tools

lost = False

#add all the other animals
loclst = ["ant","ape","badger","bafallo","bever","bull","camel","crab","cricket","crockodile","deer","dog","dolphine","doodoo","duck","elephant","fish","flamingo","giraff","gose","hedgehob","hippo","horse","kangaroo","lobstar","mosquito","otter","parrot","peacock","penguin","pig","pufferfish","rabbit","rat","rooster","scorpio","seal","shark","sheep","snail","spider","squril","stinky","turkey","turtle","whale","worm"]

cordlst = []
dub = False
hitman = []
chupper = []
name_cordinates_1 = [(375, 399),(942, 399),(1528, 399)]
name_cordinates_2 = [(375, 691),(942, 691),(1528, 691)]

Change_Reward = 0

class slot:
    def __init__(self,cor,index):
        self.cor = cor
        self.empty = True
        self.animal = None
        self.val = None
        self.index = index
    
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
    
    def upgrade(self,duplicat_position):
        pyautogui.click(duplicat_position)
        time.sleep(1)
        pyautogui.click(self.cor)
        self.val += 1

oldloc = (0,0)
slots = [slot((524,441),0), slot((671, 441),1),slot((818, 441),2),slot((965, 441),3),slot((1112, 441),4)]

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

def look_for_duplicat(name):
    for i in range(len(slots)):
        if slots[i].animal == name:
            return [True,i]
    return [False,None]

def drag_and_drop(upper : list,down: list,available_items : dict,):
    global chupper,Change_Reward

    def Reset(val):
        time.sleep(2)
        val = 0
        return val

    # Get the least-Valued token from Upper and check if down or upper is empty
    upper = check_if_empty(upper)
    down = check_if_empty(down)
    chupper = sorted(upper,key=lambda x: x[1] + x[2])

    mid = chupper[0][2] + chupper[0][1]

    # Create value list of all tokens available
    value_List = []

    for i in range(len(down)):
        value_List.append(down[i][1] + down[i][2])
    
    pop_compensator = 0
    money = 10
    


    # Placement Logic
    for i in range(len(down)):
        if down[i][1] + down[i][2] > mid or look_for_empty() == True:
            duplicatVal = look_for_duplicat(down[i][0])
            animalData = tools.fetch_animal_Value_data(down[i][0][48:len(down[i][0])-4])

            if animalData != None:
                res = tools.Adjust_Animal_Values(animalData,x)
                down[i][1] = res['stanValue']
                down[i][2] = 0

            for x in range(len(slots)):
                
                #Empty Logic
                if slots[x].empty == True and duplicatVal[0] != True and money >= 3:
                    slots[x].set((down[i][3][0] + 20,down[i][3][1] + 20),down[i][0],down[i][1] + down[i][2])
                    money -= 3
                    Change_Reward = Reset(Change_Reward)

                #Duplicat Logic
                elif duplicatVal[0] == True and money >= 3:
                    slots[duplicatVal[1]].upgrade((down[i][3][0] + 20,down[i][3][1] + 20))
                    money -= 3
                    Change_Reward = Reset(Change_Reward)

                #Replace Logic
                elif slots[x].val < down[i][1] + down[i][2] + Change_Reward and look_for_empty() == False and tools.is_best_option(slots[x],i - pop_compensator,value_List) and money >= 2:
                    slots[x].set((down[i][3][0] + 20,down[i][3][1] + 20),down[i][0],down[i][1] + down[i][2])
                    pop_compensator += 1
                    money -= 2
                    value_List.pop(i - pop_compensator)
                    Change_Reward = Reset(Change_Reward)

                else:
                    Change_Reward += 2
                
                if Change_Reward == 0:
                    break
        else:
            continue
    # Item usage Logic
    if money >= 2:
        potential_values = tools.should_use_item(slots,available_items)
        sorted_options = tools.return_best_item(potential_values)
        print(sorted_options)
        sorted_options = sorted(sorted_options,key=lambda x: x[1][1])
        i = 0
        while money >= 3 and i < len(sorted_options) - 1:
            pyautogui.click(sorted_options[i][1])
            time.sleep(1)
            pyautogui.click(slots[sorted_options[i][2]].cor)
            i += 1
            money -= 3
    
    #Charactar swap logic
    partners = tools.findSwaps(slots)
    for k in partners.keys():

        currentPartners = partners[k]
        p1D = slots[currentPartners[1]['index']]
        p2D = slots[currentPartners[0]['index']]
        transferData = [p1D.val,p1D.animal]

        slots[currentPartners[1]['index']].val = p2D.val + 2 or 0 + 2
        slots[currentPartners[1]['index']].animal = p2D.animal

        slots[currentPartners[0]['index']].val = transferData[0] or 0 + 2
        slots[currentPartners[0]['index']].animal = transferData[1]

        pyautogui.click(p1D.cor)
        time.sleep(1)
        pyautogui.click(p2D.cor)

def id_tag(location):
    name = location
    location = 'C:\\Users\\Jerome\\OneDrive\Desktop\\SAP_AI\\animals\\' + location + ".png"
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
            res = tools.fetch_animal_Value_data(name)
            if res == None:
                values = VR.find(ptlst[i])
                cordlst.append(token(location,values[0],values[1],ptlst[i]))
                continue
            else:
                val = [res["stanValue"] / 2,res["stanValue"] / 2]
                cordlst.append(token(location,val[0],val[1],ptlst[i]))

        point = ptlst[i]
        opoint = ptlst[i - 1]
        if point[0] - opoint[0] < 5:
            continue
        else:
            
            cordlst.append(token(location,1,1,point))

    cv.imwrite('res.png',img_rgb)


def start():
    global lost,cordlst,dub,hitman,chupper

    starttxt = Label(main,text="starting in 5 seconds")
    starttxt.pack()
    time.sleep(5)
    starttxt.pack_forget()
    iterations = 0
    
    while lost == False:
        available_items= IR.main()
        cordlst = []
        dub = False
        hitman = []

        scr = pyautogui.screenshot()
        scr.save("src.png")

        for loc in loclst:
            id_tag(loc)
        tokenlst = []
        
        for i in range(int(len(cordlst))):
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

        down = sorted(down,key=lambda x: x[3][0],)
        down = down[::-1]

        print("upper : {} down : {}".format(upper,down))

        drag_and_drop(upper,down,available_items)
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

        while True:
            time.sleep(10)
            scr = pyautogui.screenshot()
            scr.save("src.png")
            over = False

            src = cv.imread('src.png')
            merge_img = cv.imread('C:\\Users\\Jerome\\OneDrive\\Desktop\\SAP_AI\\recogniton_files\\over.png')
            merge_img = cv.cvtColor(merge_img, cv.COLOR_BGR2GRAY)

            img_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

            res = cv.matchTemplate(img_gray,merge_img,cv.TM_CCOEFF_NORMED)
            threshold = 0.70

            loc = np.where( res >= threshold)

            #Make functional for multiple items of the same type
            for pt in zip(*loc[::-1]):
                over = True
                break
            if over == True:
                break

        pyautogui.click(893, 428)
        time.sleep(5)
        pyautogui.click(893, 428)
        time.sleep(1)
        pyautogui.click(150,150)
        pyautogui.click(150,150)
        time.sleep(5)
    
    



b1 = Button(main,text="Begin",command=start)
b1.pack()
main.mainloop()
