#!/usr/bin/python

import csv

reader1 = csv.reader(file('test_set_18.csv', 'r'))
reader2 = csv.reader(file('result.csv', 'r'))

list_test = []
list_predict = []

for line in reader1:
    list_test.append(line)

for line in reader2:
    list_predict.append(line)

count_match = 0

for u_i in list_predict:
    if u_i in list_test:
        count_match += 1

precision = float(count_match) / len(list_predict) * 100
recall = float(count_match) / len(list_test) * 100
f1 = 2 * precision * recall / (precision + recall)

print precision
print recall
print f1
