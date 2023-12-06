import json
import os
from collections import defaultdict
import sys

def def2_value():
  return 0


def readFiles(fnum, path):
    fname1 = 'clusters50.txt'
    filepath= os.path.join(os.getcwd(), 'newApproach', path,fname1) 
    f = open(filepath)
    clusters = json.load(f)

    fname2 = 'pageranksAns_' + fnum + '.txt'
    filepath= os.path.join(os.getcwd(),'newApproach', path, 'ranked_results', fname2) 
    f = open(filepath)
    markovRank = json.load(f)

    fname3 = 'frequencYRank.txt'
    filepath= os.path.join(os.getcwd(), 'newApproach', path, 'ranked_results', fname3) 
    f = open(filepath)
    freqRank = json.load(f)

    return clusters, markovRank, freqRank


def calculate_benefit(clusters, markovRank, freqRank):
    benefit = defaultdict(def2_value)
    for key in clusters:
        for x in clusters[key]:
            s = markovRank[x]
            benefit[str(key)]+= s
    
    freqBenefit = defaultdict(def2_value)  
    for key in clusters:
        for x in clusters[key]:
            s = freqRank[x]
            freqBenefit[str(key)]+= s
    
    final_benefit = dict(sorted(benefit.items(), key=lambda k: k[1], reverse=True))  
    final_freqs = dict(sorted(freqBenefit.items(), key=lambda k: k[1], reverse=True))  
    
    return final_benefit, final_freqs


def writeToFile(data, location):
  outfile1 = open(location,'w')
  json.dump(data,outfile1,indent=2)
  outfile1.close()


def main():
    pr_w_D = float(sys.argv[1])
    path = sys.argv[2]
    fnum = str(int(pr_w_D * 100))
    clusters, markovRank, freqRank = readFiles(fnum, path)
    benefit, freqBenefit = calculate_benefit(clusters, markovRank, freqRank)

    writeToFile(benefit, os.path.join(os.getcwd(), 'newApproach', path, 'clusters', 'ranked_results', 'MarkovClusters_' + fnum + '.json'))
    writeToFile(freqBenefit, os.path.join(os.getcwd(), 'newApproach', path, 'clusters', 'ranked_results', 'FrequencyClusters.json'))
    

main()