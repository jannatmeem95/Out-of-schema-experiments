import json
import os
import sys
import numpy as np
import random
import copy
from collections import defaultdict

def readFile(fnum):
    #actual data
    if fnum < 10:
        id = '00' + str(fnum)
    else:
        id = '0' + str(fnum)
    fname1 = 'dialogues_' + id + '.json'

    filepath= os.path.join(os.getcwd(), 'input', 'dialogues', fname1) 
    f = open(filepath)
    data_actual = json.load(f)

    filepath= os.path.join(os.getcwd(), 'data', 'D-MultiWoz', fname1) 
    f = open(filepath)
    data_modified = json.load(f)

    return data_actual, data_modified


def writeToFile(data, location):
    outfile1 = open(location,'w')
    json.dump(data,outfile1,indent=2)
    outfile1.close()


def def_value():
    return list()


def get_hops_away_from_success(data_actual, data_modified, dictionary):
    t = 0
    slot_fill_count = 0
    for item_actual in data_actual:
        count = 0       
        #for item_modified in data_modified: #
        for k in range(t, len(data_modified), 1):
            item_modified = data_modified[k]
            if item_actual["dialogue_id"] == item_modified["dialogue_id"]:
                count += 1
                for i in range(len(item_actual["turns"])-1, -1, -1):
                    if "success" in item_actual["turns"][i]:
                        slots_all = set(item_actual["turns"][i-1]["frames"][0]["state"]["slot_values"].keys())
                        if len(item_modified["turns"]) > 2 and len(item_modified["turns"][len(item_modified["turns"])-2]["frames"]) > 0:
                            slots_filled = set(item_modified["turns"][len(item_modified["turns"])-2]["frames"][0]["state"]["slot_values"].keys())
                            slot_fill_count += len(slots_filled)
                            slots_left = slots_all.difference(slots_filled)
                        else:
                            slots_left = slots_all
                        base = 's' + str(len(slots_left))
                        dictionary[item_modified["turns"][len(item_modified["turns"])-2]["utterance"]].append((base, item_modified["did"]))
                        break            
            if count == 2:
                t = k
                break

    return dictionary, slot_fill_count             



def main():
    dictionary=defaultdict(def_value)
    summ=0
    q4cnt=0
  
    for p in range(1,18):
        data_actual, data_modified = readFile(p)
        summ += len(data_modified) 
        dictionary, slot_fill_count = get_hops_away_from_success(data_actual, data_modified, dictionary)
        q4cnt += slot_fill_count
    
    out_location = os.path.join(os.getcwd(), 'newApproach', 'DMultiWoz', 'conversation_sequence.json')
    writeToFile(dictionary, out_location)
    print(summ)
    print(q4cnt)

main()