#!/usr/bin/python

import csv
import cPickle as pickle

def nomalize(filename):
    reader1 = csv.reader(file(filename + '_features.csv', 'r'))
    reader2 = csv.reader(file(filename + '_features.csv', 'r'))
    reader3 = csv.reader(file(filename + '_features.csv', 'r'))
    writer1 = csv.writer(file(filename + '_nomal_features.csv', 'wb'))
#     dic_feature = pickle.load(file(filename + '.pkl', 'r'))

    for line in reader1:
        print len(line)
        maxList = []
        for i in range(len(line) - 2):
            maxList.append(0)
        break

    for line in reader2:
        for i in range(len(line) - 2):
            if float(line[i+2]) > maxList[i]:
                maxList[i] = float(line[i+2])
    print maxList
    
    for line in reader3:
        noma_list = [line[0], line[1]]
        for i in range(len(line) - 2):
            if maxList[i] != 0:
                noma_list.append(float(line[i+2]) / maxList[i])
            else:
                noma_list.append(0.0)
        writer1.writerow(noma_list)

nomalize('pos_17')
nomalize('neg_17')
nomalize('pre18_3daybefore')
