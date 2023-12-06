import json
import os
from collections import defaultdict
import numpy as np
import sys
import re

def def_value():
    return list()

def def2_value():
    return 0


def createTransitionProbDict(num_nodes,pr_s_Q,pr_Q_R,pr_W_D):
    TransitionProbs=defaultdict(def_value)

    for i in range(num_nodes): #0,1,2,3
        TransitionProbs["Q"+str(i)].append(["R"+str(i),"W"+str(i)])
        TransitionProbs["Q"+str(i)].append([pr_Q_R,1-pr_Q_R])
        if i==num_nodes-1:
            TransitionProbs["s"+str(i)].append(["success","Q"+str(i)])
        #TransitionProbs["R"+str(i)].append(["success"])
        else:
            TransitionProbs["s"+str(i)].append(["s"+str(i+1),"Q"+str(i)])
        #TransitionProbs["R"+str(i)].append(["s"+str(i+1)])
        TransitionProbs["s"+str(i)].append([1-pr_s_Q,pr_s_Q])
        TransitionProbs["R"+str(i)].append(["s"+str(i)])
        TransitionProbs["R"+str(i)].append([1])
        TransitionProbs["W"+str(i)].append(["drop","s"+str(i)])
        wD=pr_W_D#/(i+1)
        TransitionProbs["W"+str(i)].append([wD,1-wD])
    return TransitionProbs


def simulate(iteration,conversation,TransitionProbs,typeTeach): #100 iter for that particular question on that particular conversation :(slotAsked,did)
    count_success=0
    for i in range(iteration):
        next_state="s0"
        #print(conversation[1])
        if typeTeach==0:    
            
            states=[next_state,TransitionProbs[next_state][0][1],TransitionProbs[TransitionProbs[next_state][0][1]][0][1]]
        else:
            states=[next_state]
        while(True):
            next_state=np.random.choice(TransitionProbs[states[-1]][0],p=TransitionProbs[states[-1]][1])
            states.append(next_state)
            if next_state=="success":
                count_success+=1
                #print(states)
                break
            elif next_state=="drop":
                break
    return count_success


def demo(data,typeTeach,iteration,pr_s_Q,pr_Q_R,pr_W_D, outfile):
    success_dict = defaultdict(def2_value)

    #TransitionProbs=createTransitionProbDict(num_nodes,pr_s_Q,pr_Q_R,pr_W_D)
    total_simulated_convos=0
    
    for question in data:
        for i in range(len(data[question])):
            base_slot = re.findall(r'\d+', data[question][i][0]) #returns list
            num_nodes = int(base_slot[0]) + 1
            TransitionProbs=createTransitionProbDict(num_nodes,pr_s_Q,pr_Q_R,pr_W_D)
            count_success=simulate(iteration,data[question][i],TransitionProbs, 0) #typeTeach
            total_simulated_convos += iteration
            success_dict[question] += count_success
    return  success_dict, total_simulated_convos


def demo2(data,pickedQues,typeTeach,iteration,pr_s_Q,pr_Q_R,pr_W_D, success_dict, outfile): 
    #TransitionProbs=createTransitionProbDict(num_nodes,pr_s_Q,pr_Q_R,pr_W_D)
    sumCount = sum(success_dict.values())
    outfile.write("\nFor picked " + str(len(pickedQues)) + " questions:\n")
    for question in pickedQues:
        sumCount = sumCount - success_dict[question]
        count_success = 0
        for i in range(len(data[question])):
            base_slot = re.findall(r'\d+', data[question][i][0]) #returns list
            num_nodes = int(base_slot[0]) + 1
            TransitionProbs=createTransitionProbDict(num_nodes,pr_s_Q,pr_Q_R,pr_W_D)            
            val = simulate(iteration,data[question][i],TransitionProbs, typeTeach) #typeTeach
            count_success += val
            outfile.write(str(data[question][i][1])+" : ")
            outfile.write(str(val)+'\n')
        sumCount += count_success  
        #total_simulated_convos+=100*len(data[question])
    #outfile.write("\nAfter teaching: \n")
    #json.dump(success_dict,outfile,indent=2)
    return sumCount


def readFile(fnum, path):
    fname = 'conversation_sequence.json'
    filepath= os.path.join(os.getcwd(), 'newApproach', path, fname) 
    f = open(filepath)
    data = json.load(f)

    total_dialogues = 0
    for item in data:
        total_dialogues += len(data[item])

    #fname = 'MarkovClusters_' + fnum + '.json'
    filepath= os.path.join(os.getcwd(), 'newApproach', path, 'clusters', 'ranked_results', 'MarkovClusters_' + fnum + '.json')
    f = open(filepath)
    ranked_markov = json.load(f)

    fname = 'FrequencyClusters.json'
    filepath= os.path.join(os.getcwd(), 'newApproach', path, 'clusters', 'ranked_results', fname) 
    f = open(filepath)
    ranked_freq = json.load(f)

    fname1 = 'clusters50.txt'
    filepath= os.path.join(os.getcwd(),'newApproach', path, fname1) 
    f = open(filepath)
    clusters = json.load(f)

    return data, list(ranked_markov.keys()), list(ranked_freq.keys()), clusters, total_dialogues

#choice:randomly pick, Markov one, Frequency one
#for each choice, two types: don't teach(Q->R=0), teach (Q->R=1)
#for each type, three user profiles: W->D=0.1, W->D=0.5, W->D=1
def initialize(wD):
    pr_W_Ds=[wD]
    pr_Q_Rs=[0,0.2,1]
    iteration=100
    pr_q_Q=0.54
    pr_Q_R=0.2
    choices=["markov","frequency", "random"]
    return pr_W_Ds,pr_Q_Rs,iteration,pr_q_Q,pr_Q_R,choices


def main():
    wD = float(sys.argv[2])
    fnum = str( int(wD * 100) )
    path1 = sys.argv[1]
    data, topMarkovClusters, topFrequencyClusters, clusters, total_dialogues = readFile(fnum, path1)
    pr_W_Ds,pr_Q_Rs,iteration,pr_q_Q,pr_Q_R,choices=initialize(wD)

    #selected=[2,8,10,15,20]
    selected=[1, 3, 5, 8, 10, 12, 15, 17, 20]

    #location= os.path.join(os.getcwd(), 'code', 'results', 'clusters', 'simu_result_cluster_' + fnum + '.txt') 
    path = os.path.join(os.getcwd(),  'newApproach', path1, 'clusters', 'simulation_output')
    fname = 'simuResult_' + str(fnum) + '.txt'
    outfile=open(os.path.join(path,fname),"w")

    outfile.write('P(s->Q) : '+str(pr_q_Q)+'\n')
    outfile.write('P(Q->R) : '+str(pr_Q_R)+'\n')
    outfile.write('Total simulated conversations: ' + str(total_dialogues * iteration) + '\n\n')


    success_without_teaching = list()
    typeTeach = 0
    for wD in pr_W_Ds:
        successD, total = demo(data,typeTeach,iteration,pr_q_Q,pr_Q_R,wD, outfile)
        success_without_teaching.append(successD)
    print(total)

    name = 'addedSimu'+ fnum +'.txt'
    #addedFile = open(os.path.join(os.getcwd(), 'code_insert_fixed_freq', 'output', 'temp', 'didInserted', 'meaningless_removed', 'didInserted','simulation', name), "w" )
    addedFile = open(os.path.join(path, name), "w" )
    

    for k in selected:
        selected_Mclusters = topMarkovClusters[:k]
        selected_Fclusters = topFrequencyClusters[:k]

        markovQuestions = list()
        frequencyQuestions = list()

        for key in selected_Mclusters:
            markovQuestions.extend(clusters[key])

        for key in selected_Fclusters:
            frequencyQuestions.extend(clusters[key])

        outfile.write("For picked "+str(k)+" clusters:\n")
        seed_val= 7
        for category in choices:
            np.random.seed(seed_val)
            seed_val+=1
            
            outfile.write("Category: "+category+" ,\n")
            
            if category=="markov":
                pickedClusters = selected_Mclusters
                pickedQues=markovQuestions
            elif category=="frequency":
                pickedClusters = selected_Fclusters
                pickedQues=frequencyQuestions
            else:
                pickedClusters=list(np.random.choice(list(clusters.keys()),k,replace=False))
                pickedQues = list()

                for key in pickedClusters:
                    pickedQues.extend(clusters[key])

        
            for w in range(len(pickedQues)):
                times=len(data[pickedQues[w]])*iteration 
            
            summ = 0
            for key in pickedQues:
                summ += len(data[key])

            outfile.write("No. of Clusters: "+str(pickedClusters)+", No. of Questions : " + str(summ)+ "\n")

            for p in range(len(pr_W_Ds)):
                outfile.write("\t\t P(W->D):"+str(pr_W_Ds[p])+': \n')
                typeTeach = 0
                outfile.write("\t\t\t PR(Q->R): "+ str(0))
                    
                success_count1 = sum(success_without_teaching[p].values())
                outfile.write("----> Total Successful Convo: "+str(success_count1)+"\n")
                                    
                outfile.write("\t\t\t PR(Q->R): "+ str(1))
                success_count2 = demo2(data, pickedQues, 1,iteration,pr_q_Q,pr_Q_R,pr_W_Ds[p], success_without_teaching[p], addedFile)  
                outfile.write("----> Total Successful Convo: "+str(success_count2)+"\n\n")

                outfile.write("Success rate: " + str((success_count2 - success_count1)/success_count1) + '\n\n')
                 
    outfile.close()

main()