import csv
import numpy as np
import cPickle as pickle
from sklearn.linear_model import LogisticRegression

reader = csv.reader(file('pre18_3daybefore_nomal_features.csv','r'))
writer = csv.writer(file('result.csv', 'wb'))

features = []
ui = []
for line in reader:
    for i in range(2, len(line)):
        line[i] = np.float32(line[i])
    features.append(line[2:])
    ui.append(line[:2])
    
def predict(num):
    model_file = file('model/lr' + str(num) + '.pkl','rb')
    lr = pickle.load(model_file)
    
    cluster = lr.predict_proba(features)        #save the cluster result, e.g. cluster[j][i] represents the jth lr predicts the ith sample
    dic_cluster[num] = cluster


times = 50

dic_cluster = {}
for i in range(0, times):
    predict(i)
    
for i in range(len(dic_cluster[0])):
    Sum = 0
    for j in range(0, times):
        Sum += dic_cluster[j][i][1]
    ave = Sum / times
    if ave >= 0.72:
        writer.writerow(ui[i])
#        print ui[i]

