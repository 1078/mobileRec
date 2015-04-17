#!/usr/bin/python
# -*-coding:utf-8-*-

import csv
import os
import readMultiCSVFile as rmf

class extractFeaturesNTags(object):

    def __init__(self, input_dir, output_dir, tag_date, pre_date, time_window):
        self.input_dir = input_dir   # split_data/
        output_path = output_dir + 'pre' + pre_date.split('-')[-1] + os.sep   # features/(pre1219/)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        self.output_dir = output_path
        self.tag_date = tag_date
        self.pre_date = pre_date
        self.time_window = time_window

        self.windowReader = rmf.readMultiCSVFile(input_dir, tag_date, '%Y-%m-%d', time_window)

        self.dic_uBehaviorCount = {}   # {id:[[1,2,3,4], [], []]}
        self.dic_iBehaviorCount = {}
        self.dic_cBehaviorCount = {}
        
        self.dic_uRebuyRate = {}   # {id:}
        self.dic_iRebuyRate = {}
        self.dic_cRebuyRate = {}

        self.dic_uTransferRate = {}
        self.dic_iTransferRate = {}
        self.dic_cTransferRate = {}

        self.dic_uiBehaviorCount = {}
        self.dic_ucBehaviorCount = {}

        self.dic_uiCartNotBuy = {}
        self.dic_ucCartNotBuy = {}

    def _uicBehaviorCount(self):
        '''Count each behavior of user/item/category of each day in the time_window.'''
        csv_feature_reader_list = self.windowReader._readFeatureSet()

        for i in range(self.time_window):
            for line in csv_feature_reader_list[i]:
                userid = line[0]
                itemid = line[1]
                catid = line[4]
                behavior = line[2]
        
                if not self.dic_uBehaviorCount.has_key(userid):
                    self.dic_uBehaviorCount[userid] = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                self.dic_uBehaviorCount[userid][i][int(behavior) - 1] += 1

                if not self.dic_iBehaviorCount.has_key(itemid):
                    self.dic_iBehaviorCount[itemid] = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                self.dic_iBehaviorCount[itemid][i][int(behavior) - 1] += 1

                if not self.dic_cBehaviorCount.has_key(catid):
                    self.dic_cBehaviorCount[catid] = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
                self.dic_cBehaviorCount[catid][i][int(behavior) - 1] += 1

    def _uicRebuyRate(self):
        '''Calculate rebuy rate of user/item/category in time window'''



# test
# a = extractFeaturesNTags('split_data/', 'features/', '2014-12-01', '2014-12-19', 3)
# a._uicBehaviorCount()
# print len(a.dic_uBehaviorCount)
