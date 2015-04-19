#coding=utf-8

import readMultiCSVFile as rmf
import os
import csv
import random
import numpy as np
import discrete
import cPickle as pickle
import sys
from sklearn.linear_model import LogisticRegression

def sample_data( input_dir, output_file, sample_ratio, X, y ):
    reader_list = []
    for f in os.listdir(input_dir):
        if os.path.isfile(os.path.join(input_dir, f)):
            reader_list.append(csv.reader(file(os.path.join(input_dir, f),'r')))
    #sample
    for reader in reader_list:
        for line in reader:
            num_list = [float(f) for f in line]
            rand_score = 0
            if num_list[0] == 1 or random.random() < sample_ratio:
                y.append(num_list[0])
                X.append(num_list[3:])

def descrete_set( train_path, test_path,
        discrete_train_file, discrete_test_file,
        seperator, col_num, discrete_num=10, except_list=()):
    #get boundary
    slice_boundary = discrete.get_boundary( train_path, seperator, col_num, discrete_num, except_list )
    #discrete train_set
    discrete.discrete_feature(slice_boundary,train_path,discrete_train_file,seperator,col_num,discrete_num,except_list)
    #discrete train_set
    discrete.discrete_feature(slice_boundary,test_path,discrete_test_file,seperator,col_num,discrete_num,except_list)



X = []
y = []
sample = []
lr =LogisticRegression(class_weight='auto',C=0.1)


# descrete_set('features/pre18/train/', 'features/pre18/pre/',
#              'features/pre18/discrete_train','features/pre18/discrete_test',
#              ',', 60, 10, (0,))

sample_data('features/pre18/train/', 'features/pre18/sample_train', 0.5, X, y)

lr.fit(X,y)
f_model = file('model/lr_0.5.pkl','wb')
pickle.dump(lr,f_model)
