# Funktions for the Ai Stored in this script to make the main script less messy :)
import json

#time O(1) Space O(1) | Constant Time && Space
def is_best_option(slot,downIndex,value_List):

    if value_List[downIndex] == max(value_List) and max(value_List) > slot.val:
        return True
    else:
        return False

#Time O(1) Space O(1) | Constant Space && Time
def fetch_animal_Value_data(Animal):
    json_File = open('animalValues.json')
    animal_Values = json.load(json_File)

    name = Animal[0]
    name = name[48:len(name)-4]

    try:
        return animal_Values[name]
    except:
        return None


#Time O(n)  n = len(animal_Values) Space O(n) n = animal_Values | liniar Time
def Adjust_Animal_Values(animal_Values,current_slot_index):
    for key in animal_Values.keys():
        if animal_Values[key] == None:
            continue

        if key == 'preffedPos':
            if current_slot_index in animal_Values[key]:
                animal_Values['stanValue'] += 3

        elif key == 'badPos':
            if current_slot_index in animal_Values[key]:
                animal_Values['stanValue'] -= 3
        
        elif key == 'vorbidenPos':
            if current_slot_index in animal_Values[key]:
                animal_Values['stanValue'] = -99
    
    return animal_Values

def should_use_item(token_lst,items):
    val_Lst = {}

    for token in token_lst:
        val_Lst[token.index] = {}
        for k in items.keys():
            current_item = items[k]
            cal = token.val
            if cal == None:
                cal = 0

            val_Lst[token.index][current_item[1]] = eval(str(str(cal) + str(current_item[0])))
    
    return val_Lst
    
def return_best_item(potential_values):
    val_list = []
    for key in potential_values.keys():
        try:
            sub_key = list(potential_values[key].keys())[0]
        except:
            break
        val_list.append([potential_values[key][sub_key],sub_key,key])
    val_list = sorted(val_list,key = lambda x: x[0],reverse=True)

    return val_list
        

