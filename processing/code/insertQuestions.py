import json
import os
from collections import defaultdict
import sys
import copy
import random
import numpy as np


def readFile(fnum):
    if fnum < 10:
        id = '00' + str(fnum)
    else:
        id = '0' + str(fnum)
    fname1 = 'dialogues_' + id + '.json'
    filepath= os.path.join(os.getcwd(), 'input', 'dialogues', fname1) 
    f = open(filepath)
    data = json.load(f)

    return data



def readQuestions(fname): 
    filepath = os.path.join(os.getcwd(), 'ques_to_be_inserted', 'questions', fname) 
    f = open(filepath,'r')
    lines = f.readlines()
    
    questions=dict()
    for i in range(0, len(lines)-1, 4):
        questions[lines[i].strip()]=[]
        for j in range(4):
            questions[lines[i].strip()].append(lines[i+j].strip())
    return questions


def getQuestion(fname):
    questions = readQuestions(fname)
    ques_rank = np.random.choice(list(questions.keys())) 
    ques_choice = np.random.choice(questions.get(ques_rank))

    return ques_choice


def pickQuestion(picked_category):
    if picked_category=="restaurant-area":
        ques = getQuestion("area.txt")       
    elif picked_category== "restaurant-food":
        ques = getQuestion("food.txt")        
    elif picked_category=="restaurant-pricerange" :
        ques = getQuestion("price.txt")
    elif picked_category=='restaurant-name':
        ques = getQuestion("restaurantName.txt")
    elif picked_category == "starting":
        ques = getQuestion("startingQ.txt")

    return ques




        #copy

def insertQues(data):
    dialogues_after_insertion=[]
    count = 0
    dam_count = 0
    slots=['restaurant-area','restaurant-food','restaurant-pricerange','restaurant-name']

    for dialogue in data: 
        #print("inside x")
        again=False

        turns=copy.deepcopy(list(dialogue['turns']))
        #print("first turn: "+str(len(turns)))

        while True:
            x=copy.deepcopy(dialogue)
            x['turns']=copy.deepcopy(turns)
            discard=1
            if again==True:
                start=1
            else:
                start=0

            while discard == 1:
                if len(x['turns'])%2==0:
                    position= random.randint(start, (len(x['turns'])/2)-1)*2
                else:
                    position= random.randint(start, (len(x['turns'])-1)/2)*2    
                if position ==0 or "success" not in x['turns'][position-1]:
                    discard =0
                #'restaurant-area' in x['turns'][0]['frames'][0]['state']['slot_values'].keys() or x['turns'][position-1]['frames'][0]['slots'][0]['slot']=='restaurant-name'
                # 
            if x['turns'][position-2]['frames'][0]['state']['active_intent']!="NONE" or position!=0:
                filledSlots=[]

                for slot in slots:
                    if (slot in x['turns'][position-2]['frames'][0]['state']['slot_values'].keys()) or (slot== 'restaurant-name' and ((len(x['turns'][position-1]['frames'])!=0 and x['turns'][position-1]['frames'][0]['slots'][0]['slot']==slot) or (x['turns'][position-2]['frames'][0]['state']['active_intent']=="book_restaurant"))):
                        filledSlots.append(slot)

                if len(filledSlots)!=0:
                    category = random.randint(0, (len(filledSlots)-1))
                    ques = pickQuestion(filledSlots[category])  
                else:
                    ques = pickQuestion("starting")
                
            else:
                ques = pickQuestion("starting")
            
            if position!=0:
                #print("inside false")
                prev_user_turn=x['turns'][position].copy()
                x['turns'][position]=x['turns'][position-2].copy()
                x['turns'][position]['utterance']=ques #position-1 er copy hobe
                x['turns'][position]['turn_id']=prev_user_turn['turn_id']
                again=False
                count += len(x['turns'][position]['frames'][0]['state']['slot_values'])
                
            else:
                if len(x['turns'])>2:
                        again=True
                x['turns'][position]=x['turns'][position].copy()
                x['turns'][position]['utterance']=ques
                x['turns'][position]['frames']=[]
                count +=1

                #dropout
            if position != (len(x['turns'])-1):
                prev_system_turn=x['turns'][position+1].copy()
                if position!= 0:
                    turnId = x['turns'][position+1]['turn_id']
                    x['turns'][position+1]=x['turns'][position-1].copy()
                    x['turns'][position+1]['turn_id']=turnId
                else:
                    x['turns'][position+1]['frames']=[]
                    
                x['turns'][position+1]['utterance']="I don't know."
                del x['turns'][position+2:]  
            
            else:     
                temp=x['turns'][position-1].copy()
                temp['utterance']="I don't know."
                x['turns'].append(temp)
                dam_count+=1
                
            dialogues_after_insertion.append(x)
            if again== False:
                break
    return dialogues_after_insertion, count, dam_count


def writeToFile(data, fnum):
    if fnum < 10:
        id = '00' + str(fnum)
    else:
        id = '0' + str(fnum)
    fname1 = 'dialogues_' + id + '.json'
    filepath= os.path.join(os.getcwd(), 'processing', 'inserted_dialogues', fname1) 
    f = open(filepath, 'w')
    json.dump(data , f, indent=6)


def default_value():
    return 0


def main():
    total_filled_slots = 0
    nom = 0
    for p in range(1,18):
        data = readFile(p)
        dialogues_after_insertion, current_filled_slots, dam_count = insertQues(data)
        nom += len(dialogues_after_insertion)
        total_filled_slots += current_filled_slots
        writeToFile(dialogues_after_insertion, p)
        print("yoooo "+str(p))

    print("Total dialogues: " + str(nom))
    print("Number of filled slots: " + str(total_filled_slots))
    print(nom/total_filled_slots)
    
main()
