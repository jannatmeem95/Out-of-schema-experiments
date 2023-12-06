import json
import os
from collections import defaultdict
import sys
import copy
import random
import numpy as np


def insert_did(data, did):
    dialogues_after_insertion=[]
    for dialogue in data: 
        dialogue['did']=did
        did += 1
        dialogues_after_insertion.append(dialogue)
    return dialogues_after_insertion,did

def readFile(fnum):
    if fnum < 10:
        id = '00' + str(fnum)
    else:
        id = '0' + str(fnum)
    fname1 = 'dialogues_' + id + '.json'
    filepath= os.path.join(os.getcwd(), 'processing', 'inserted_dialogues', fname1) 
    f = open(filepath)
    data = json.load(f)

    return data

def writeToFile(data, fnum):
    if fnum < 10:
        id = '00' + str(fnum)
    else:
        id = '0' + str(fnum)
    fname1 = 'dialogues_' + id + '.json'
    filepath= os.path.join(os.getcwd(), 'data', 'D-MultiWoz', fname1) 
    f = open(filepath, 'w')
    json.dump(data , f, indent=6)

def main():
    did = 0
    for p in range(1,18):
        data = readFile(p)
        dialogues_after_insertion, did = insert_did(data, did)
        writeToFile(dialogues_after_insertion, p)
        print("yoooo "+str(p))
    print(did-1)

main()