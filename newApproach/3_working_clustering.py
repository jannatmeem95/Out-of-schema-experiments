#!pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from collections import defaultdict
import json


model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def readFile(location):
  f = open(location)
  data = json.load(f)
  return data

def writeToFile(data, location):
  outfile1 = open(location,'w')
  json.dump(data,outfile1,indent=2)
  outfile1.close()


path = sys.argv[1]  #DMultiWoz or DSGD

prs=readFile(os.path.join(os.getcwd(), 'newApproach', path, 'conversation_sequence.json'))
text=prs.keys()
data=dict()
data['text']=list(text)
print(len(data['text']))


#Sentences are encoded by calling model.encode()
data['embeddings'] = model.encode(data['text'])

X = np.array(data['embeddings'])
pca = PCA(n_components=2)
pca.fit(X.T)
components=pca.components_.T

distortions = []

K = range(1, 80)

for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(X) #X=data['embeddings']
    distortions.append(kmeanModel.inertia_)

plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')

plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()

kmeanModel = KMeans(n_clusters=50)
kmeanModel.fit(X)
data['k_means']=kmeanModel.predict(X)
data['clusters']=kmeanModel.labels_



def def_value():
    return list()

d = defaultdict(def_value)


for i in range (len(data['clusters'])):
  d[int(data['clusters'][i])].append(data['text'][i])
  

writeToFile(d, os.path.join(os.getcwd(), 'newApproach', path, 'clusters50.txt'))

