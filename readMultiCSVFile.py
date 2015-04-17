#coding:utf-8
__author__ = 'luolan.ll'

import csv
import time
import os

class readMultiCSVFile(object):

    def __init__(self, input_dir, date, time_pattern, time_window):
        self.time_pattern = time_pattern
        self.time_window = time_window
        self.input_dir = input_dir
        self.tag_date = time.strptime(date, time_pattern)
        self.tag_keys = []
        self.tag_file = os.path.join(self.input_dir, date)
        self.feature_file_list = []
        for f in os.listdir(self.input_dir):
            if os.path.isfile(os.path.join(self.input_dir, f)) \
                and time.mktime(self.tag_date)-time.mktime(time.strptime(f, time_pattern)) <= time_window*3600*24 \
                and time.mktime(self.tag_date)-time.mktime(time.strptime(f, time_pattern)) > 0:
                self.feature_file_list.append(os.path.join(self.input_dir, f))

        self.ui_dict = {}
        self.user_dict = {}
        self.item_dict = {}

    # load feature files as u-i dict
    def _loadFeatureSet(self):
        for f in self.feature_file_list:
            csv_reader = csv.reader(file(f, 'r'))
            for line in csv_reader:
                if len(line) != 6:
                    continue
                # ui dict
                if self.ui_dict.has_key((line[0], line[1])):
                    self.ui_dict[(line[0], line[1])].append((line[2], line[4], line[5]))
                else:
                    self.ui_dict[(line[0], line[1])] = [(line[2], line[4], line[5])]
                # user dict
                # if self.user_dict.has_key(line[0]):
                #     self.ui_dict[line[0]].append((line[2], line[5]))
                # else:
                #     self.ui_dict[line[0]] = [(line[2], line[5])]

    # return feature file name list
    def _get_feature_file_list(self):
        return self.feature_file_list				

    # return tag file csv reader
    def _readTagSet(self):
        return csv.reader(file(self.tag_file, 'r'))

    # return feature file csv reader list
    def _readFeatureSet(self):
        csv_reader_list = []
        for f in self.feature_file_list:
            csv_reader_list.append(csv.reader(file(f, 'r')))
        return csv_reader_list

# test
# a=readMultiCSVFile('split_data/','2014-12-01','%Y-%m-%d',3)
# print a._get_feature_file_list()
# print a._readFeatureSet()
# print a._readTagSet()
# a._loadFeatureSet()
# print len(a.ui_dict)
