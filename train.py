import numpy as np
import csv
import random
import cPickle as pickle
import sys
from sklearn.linear_model import LogisticRegression

def train(num):
    negReader = csv.reader(file('neg_17_nomal_features.csv','r'))
    posReader = csv.reader(file('pos_17_nomal_features.csv','r'))
    lr =LogisticRegression(class_weight='auto',C=0.1)
    Xbr = []
    ybr = []
    
    for line in negReader:
        ybr.append(0)
        Xbr.append(line[2:])
    
    X = random.sample(Xbr, 3320)
    y = random.sample(ybr, 3320)
    
    for line in posReader:
        y.append(1)
        X.append(line[2:])
    lr.fit(X,y)
    f_model = file('model/lr' + str(num) + '.pkl','wb')
    pickle.dump(lr,f_model)

for i in range(0, 100):
    train(i)
