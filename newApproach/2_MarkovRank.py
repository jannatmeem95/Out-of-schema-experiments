

import json
import os
import sys
import numpy as np
import random
import copy
from collections import defaultdict
import re

#---------ADJACENCY MATRIX----------
def initialize(num_questions,base):
  rows=num_questions*4+2    # +2 for final state,then dropout state, each q has 4 states associated: qi,Qi,Ri,Wi
  columns=num_questions*4+2
  M= np.zeros(shape=(rows,columns))

  #----------INITIAL PAGERANKS--------
  r = np.ones((columns,1))

  #--------------BASE SET-------------
  E=np.zeros(shape=(columns,1))
  E[base*4]=1

  return M,E,r


#------------POPULATE EDGE VALUES INTO THE ADJACENCY MATRIX----------------
def populate_adjMat(M,pr_W1_D,pr_Q1_R1,q_prob,num_questions):
  x=1
  for i in range(0,num_questions*4,4):  #for all outgoing edge from all qi
    M[i][i+1]=q_prob
    M[i][x*4]= 1-q_prob  #qi->q(i+1)
    x+=1

  for i in range(1,num_questions*4,4):  #for all outgoing edge from all Qi
    M[i][i+1]=pr_Q1_R1
    M[i][i+2]=1.0 - pr_Q1_R1
    
  for i in range(2,num_questions*4,4):  #for all outgoing edge from all Ri
    M[i][i-2]=1
    
  for i in range(3,num_questions*4,4):  #for all outgoing edge from all Wi
    M[i][i-3]=1 - pr_W1_D
    M[i][num_questions*4+1]=pr_W1_D
  
  return M

#---------ADJACENCY MATRIX----------
def initializeNotAns(num_questions,base):
  rows=num_questions*4+3    # +2 for final state,then dropout state, each q has 4 states associated: qi,Qi,Ri,Wi
  #extra state for initial W (W->q, W->D)
  columns=num_questions*4+3
  M= np.zeros(shape=(rows,columns))

  #----------INITIAL PAGERANKS--------
  r = np.ones((columns,1))

  #--------------BASE SET-------------
  E=np.zeros(shape=(columns,1))
  E[columns-1]=1  # W, where question was asked but not responded (first W)
  
  return M,E,r

#------------POPULATE EDGE VALUES INTO THE ADJACENCY MATRIX----------------
def populate_adjMatNotAns(M,pr_W1_D,pr_Q1_R1,q_prob,num_questions):
  x=1
  for i in range(0,num_questions*4,4):  #for all outgoing edge from all qi
    M[i][i+1]=q_prob #qi->Qi
    M[i][x*4]=  1-q_prob  #qi->q(i+1)
    x+=1

  for i in range(1,num_questions*4,4):  #for all outgoing edge from all Qi
    M[i][i+1]=pr_Q1_R1
    M[i][i+2]=1.0 - pr_Q1_R1
    
  for i in range(2,num_questions*4,4):  #for all outgoing edge from all Ri
    M[i][i-2]=1
    
  for i in range(3,num_questions*4,4):  #for all outgoing edge from all Wi
    M[i][i-3]=1 - pr_W1_D
    M[i][num_questions*4+1]=pr_W1_D  #index of D state: num_questions*4+1
  #M[num_questions*4][num_questions*4]=1-q_prob
  
  # for all outgoing edges from W; W->D, W->q0 (q0 because nodes before are curtailed)
  M[M.shape[1]-1][num_questions*4+1] = pr_W1_D
  M[M.shape[1]-1][0] = 1 - pr_W1_D
  return M



def pagerank(M,E,r,d):
  while(True):
    prev_r=r
    r=(1-d)*E + d*np.dot(M,r)
    if np.allclose(r, prev_r, rtol=1e-03, equal_nan=False) or np.allclose(prev_r, r, rtol=1e-03, equal_nan=False):   
      return r


def def2_value():
  return 0


def writeToFile(data, location):
  outfile1 = open(location,'w')
  json.dump(data,outfile1,indent=2)
  outfile1.close()


def callFunc(d, probD, probC, q_prob, dictionary, option, fnum, path):
  
  new_dict=defaultdict(def2_value)  #total benefit(PR) for each question
  new_dict3=defaultdict(def2_value) ##total freq(at q3) for each question

  ########
  
  dict_Q_coversationID_PR = dict()
  if option == 'r':   
    outLocation = os.path.join(os.getcwd(), 'newApproach', path, 'extra', 'dict_Q_convoID_PR_Ans5'+ str(fnum)+ '.txt')
  else:
    outLocation = os.path.join(os.getcwd(), 'newApproach', path, 'extra', 'dict_Q_convoID_PR_NotAns5'+ str(fnum)+ '.txt')
  outfile = open(outLocation,'w') 
  
  ########
  for x in dictionary: #x ->Question
    ######
    dict_Q_coversationID_PR[x] = dict()
    #outfile.write(x+":{\n")
    ######
    for i in range(len(dictionary[x])): #dictionary[x] -> list of (base,did)
      #if dictionary[x][i][0]=='q3':
      base_slot = re.findall(r'\d+', dictionary[x][i][0]) #returns list
      num_questions = base_slot[0]
      #b=slotids[base_slot]
      n = int(num_questions)
      if option == 'r':
        M,E,r=initialize(n,0)
        M=populate_adjMat(M,probD,probC,q_prob,n)   #k=dropout, c= bot correct answer        
      else:
        M,E,r=initializeNotAns(n,0)
        M=populate_adjMatNotAns(M,probD,probC,q_prob,n)
        #print(M.shape)
      
      r=pagerank(M.T,E,r,d)   #initialized M with rows with columns and cols with rows, so Transpose before pagerank
      
      pos=n*4 #success state
     
      tmp=r.tolist()[pos]
      
      #######

      dict_Q_coversationID_PR[x][str(dictionary[x][i])] = tmp[0]
      
      #######

      new_dict[x]+= tmp[0]   #PR of success state
      new_dict3[x]+=1
    

    outfile.write(x+"{\n")
    json.dump(dict_Q_coversationID_PR[x],outfile,indent=2)
    outfile.write("}\n")
    
    #########

  final_benefit = dict(sorted(new_dict.items(), key=lambda k: k[1], reverse=True))
  if option == 'r':
    fname = 'pageranksAns_' + str(fnum) + '.txt'
    writeToFile(final_benefit,os.path.join(os.getcwd(), 'newApproach', path, 'ranked_results' , fname))
  else:
    fname = 'pageranksNotAns_' + str(fnum) + '.txt'
    #writeToFile(final_benefit,os.path.join(os.getcwd(), 'code_insert_fixed_freq', 'output', 'temp', 'didInserted', 'meaningless_removed', 'didInserted', fname))
  final_benefit2 = dict(sorted(new_dict3.items(), key=lambda k: k[1], reverse=True))
  writeToFile(final_benefit2,os.path.join(os.getcwd(), 'newApproach', path, 'ranked_results', 'frequencYRank.txt'))
  
  return final_benefit


def main():
    pr_w_d = float(sys.argv[1]) #025/ 0.5/ 0.75/ 0.9
    fnum = int(pr_w_d * 100)

    q_prob = float(sys.argv[2]) #0.2/ 0.5
    path = sys.argv[3]  #DMultiWoz or DSGD


    filepath= os.path.join(os.getcwd(), 'newApproach', path, 'conversation_sequence.json') 
    f = open(filepath)
    data = json.load(f)  #dictionary

    d = 0.9999
    probD = pr_w_d #any_D
    probC = 0.5 #Q->R
    #q_prob = 0.54 #523/973

    ############
    dict1 = callFunc(d, probD, probC, q_prob, data, 'r', fnum, path)
    #dict2 = callFunc(d, probD, probC, q_prob, num_questions, data, 'w', fnum)
    #calculateDifference(dict1, dict2, fnum)
    #calculateDifference(dict1,dict2)

main()
