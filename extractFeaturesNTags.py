#!/usr/bin/python
# -*-coding:utf-8-*-

import csv
import os
import readMultiCSVFile as rmf

class extractFeaturesNTags(object):

    def __init__(self, ori_dir, split_dir, output_dir, tag_date, pre_date, time_window):
        self.ori_dir = ori_dir   # ori_data/
        self.split_dir = split_dir   # split_data/
        output_path = output_dir + 'pre' + pre_date.split('-')[-1] + os.sep   # features/(pre1219/)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        self.output_dir = output_path
        self.tag_date = tag_date
        self.pre_date = pre_date
        self.time_window = time_window

        self.windowReader = rmf.readMultiCSVFile(split_dir, tag_date, '%Y-%m-%d', time_window)
        
        ## item and cat dict of subset
        self.dic_item = {}   # {itemid:[cat, geo]}
        self.dic_cat = {} # {cat:1}

        ## feature dict
        self.dic_uBehaviorCount = {}   # {id:[[1,2,3,4], [], []]}
        self.dic_iBehaviorCount = {}
        self.dic_cBehaviorCount = {}
        
        self.dic_uRebuyRate = {}   # {id:rebuyRate}
        self.dic_iRebuyRate = {}
        self.dic_cRebuyRate = {}

        self.dic_uTransferRate = {}   # {uid:[4/1,4/2,4/3]}
        self.dic_iTransferRate = {}
        self.dic_cTransferRate = {}

        self.dic_uiBehaviorCount = {}   # {(uid,iid):[1,2,3,4]}
        self.dic_ucBehaviorCount = {}

        self.dic_uiCartNotBuy = {}   # {(uid,iid):[1,1,1]}
        self.dic_ucCartNotBuy = {}

        self.dic_allfeatures = {}
        self.dic_nomalfeatures = {}

        ## temp dict of counting
        self.dic_ub = {}   # user buy {uid:[iid,iid,...]}
        self.dic_urb = {}   # user rebuy
        self.dic_ib = {}
        self.dic_irb = {}
        self.dic_cb = {}
        self.dic_crb = {}

        self.dic_ut_temp = {}   # user transfer temp {uid:[[4,1],[4,2],[4,3]]}
        self.dic_it_temp = {}
        self.dic_ct_temp = {}

        ## u-i couple dict
        self.dic_train = {}   # {(uid,iid):1 or 0}
        self.dic_pre = {}


    
    def getItemDict(self):
        '''Load the item file into a dict'''
        item_reader = csv.reader(file(self.ori_dir + 'tianchi_mobile_recommend_train_item.csv', 'r'))
        for line in item_reader:
            if line[0] not in self.dic_item:
                self.dic_item[line[0]] = [line[2], line[1]]
            if line[2] not in self.dic_cat:
                self.dic_cat[line[2]] = 1
        
    
    ## behavior count for each day
    def behaviorCountJudge(self, key, day, behavior, dic):
	if key not in dic:
	    dic[key] = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        dic[key][day][int(behavior) - 1] += 1
	
    def uicBehaviorCount(self, userid, itemid, catid, behavior, day):
        '''Count each behavior of user/item/category of each day in the time_window.'''
        self.behaviorCountJudge(userid, day, behavior, self.dic_uBehaviorCount)
        if itemid in self.dic_item:
            self.behaviorCountJudge(itemid, day, behavior, self.dic_iBehaviorCount)
        if catid in self.dic_cat:
	    self.behaviorCountJudge(catid, day, behavior, self.dic_cBehaviorCount)
		
	
    ## rebuy rate
    def rebuyCountJudge(self, key, value, dict_b, dict_rb):
        if key not in dict_b:
	    dict_b[key] = [value]
	else:
            if value not in dict_b[key]:
                dict_b[key].append(value)
            else:
                if key not in dict_rb:
                    dict_rb[key] = [value]
                elif value not in dict_rb[key]:
                    dict_rb[key].append(value)
	
    def uicRebuyCount(self, userid, itemid, catid, behavior):
        '''count the rebuy of user/item/category in time window'''
        if behavior == '4':
            self.rebuyCountJudge(userid, itemid, self.dic_ub, self.dic_urb)
            if self.dic_item.has_key(itemid):
                self.rebuyCountJudge(itemid, userid, self.dic_ib, self.dic_irb)
            if self.dic_cat.has_key(catid):
                self.rebuyCountJudge(catid, userid, self.dic_cb, self.dic_crb)
	
    def rebuyRateCalculate(self, dict_b, dict_rb, dict_rate):
        for key in dict_b:
            if key in dict_rb:
                dict_rate[key] = float(len(dict_rb[key])) / float(len(dict_b[key]))
            else:
                dict_rate[key] = 0

    def uicRebuyRate(self):
        '''Calculate the rebuy rate after counting all the rebuy'''
        self.rebuyRateCalculate(self.dic_ub, self.dic_urb, self.dic_uRebuyRate)
        self.rebuyRateCalculate(self.dic_ib, self.dic_irb, self.dic_iRebuyRate)
        self.rebuyRateCalculate(self.dic_cb, self.dic_crb, self.dic_cRebuyRate)


    ## u-i, u-c Behavior count
    def uiucBehaviorCount(self, userid, itemid, catid, behavior):
        '''Count the behavior of u-i/u-c'''
        if itemid in self.dic_item:
            if (userid, itemid) not in self.dic_uiBehaviorCount:
                self.dic_uiBehaviorCount[(userid, itemid)] = [0,0,0,0]
            self.dic_uiBehaviorCount[(userid, itemid)][int(behavior) - 1] += 1

            if (userid, self.dic_item[itemid][0]) not in self.dic_ucBehaviorCount:
                self.dic_ucBehaviorCount[(userid, self.dic_item[itemid][0])] = [0,0,0,0]
            self.dic_ucBehaviorCount[(userid, self.dic_item[itemid][0])][int(behavior) - 1] += 1


    ## transfer rate
    def uiTransferTemp(self, key, value, dic_temp):
        if key not in dic_temp:
            dic_temp[key] = [[0,0],[0,0],[0,0]]
        for i in range(3):
            if value[i] >= value[3]:
                dic_temp[key][i][0] += value[3]
            else:
                dic_temp[key][i][0] += value[i]
            dic_temp[key][i][1] += value[i]

    def uicTransferCount(self):
        '''count the transfer of user/item/category in time window'''
        for (k, v) in self.dic_uiBehaviorCount.items():
            self.uiTransferTemp(k[0], v, self.dic_ut_temp)
            self.uiTransferTemp(k[1], v, self.dic_it_temp)
        for (k, v) in self.dic_it_temp.items():
            if self.dic_item[k][0] not in self.dic_ct_temp:
                self.dic_ct_temp[self.dic_item[k][0]] = [[0,0],[0,0],[0,0]]
            for i in range(3):
                for j in range(2):
                    self.dic_ct_temp[self.dic_item[k][0]][i][j] += v[i][j]

    def calculateTrRate(self, dic_temp, dic_rate):
        for (k, v) in dic_temp.items():
            if k not in dic_rate:
                dic_rate[k] = [0,0,0]
            for i in range(3):
                if v[i][1] == 0:
                    dic_rate[k][i] = 0
                else:
                    dic_rate[k][i] = float(v[i][0]) / float(v[i][1])

    def uicTransferRate(self):
        '''Calculate teh transfer rate of user/item/category in time window'''
        self.calculateTrRate(self.dic_ut_temp, self.dic_uTransferRate)
        self.calculateTrRate(self.dic_it_temp, self.dic_iTransferRate)
        self.calculateTrRate(self.dic_ct_temp, self.dic_cTransferRate)


    ## u-i, u-c cart not buy
    def uiucCartNotBuy(self, userid, itemid, catid, day, behavior):
        '''judge if the u-i/u-c was put in cart and has not been bought in the time window for each day'''
        if itemid in self.dic_item and behavior == '3' and self.dic_uiBehaviorCount[(userid, itemid)][3] == 0:
            if (userid, itemid) not in self.dic_uiCartNotBuy:
                self.dic_uiCartNotBuy[(userid, itemid)] = [0,0,0]
            self.dic_uiCartNotBuy[(userid, itemid)][day] = 1
        if itemid in self.dic_item and behavior == '3' and self.dic_ucBehaviorCount[(userid, catid)][3] == 0:
            if (userid, catid) not in self.dic_ucCartNotBuy:
                self.dic_ucCartNotBuy[(userid, catid)] = [0,0,0]
            self.dic_ucCartNotBuy[(userid, catid)][day] = 1
            
    
    ## extract tag data
    def extractTrainUi(self, userid, itemid, behavior):
        if itemid in self.dic_item:
            if (userid, itemid) not in self.dic_train:
                if behavior == '4':
                    self.dic_train[(userid, itemid)] = 1
                else:
                    self.dic_train[(userid, itemid)] = 0
            else:
                if behavior == '4':
                    self.dic_train[(userid, itemid)] = 1

    def extractPreUi(self, userid, itemid, behavior):
        if itemid in self.dic_item:
            if (userid, itemid) not in self.dic_pre:
                self.dic_pre[(userid, itemid)] = ''
         

    def firstReader(self):
        csv_feature_reader_list = self.windowReader._readFeatureSet()
        for day in range(self.time_window):
            for line in csv_feature_reader_list[day]:
                userid = line[0]
                itemid = line[1]
                behavior = line[2]
                catid = line[4]
                date = line[5].split(' ')[0]
                time = int(line[5].replace('-', '').replace(' ', ''))
                
                self.uicBehaviorCount(userid, itemid, catid, behavior, day)
                self.uicRebuyCount(userid, itemid, catid, behavior)
                self.uiucBehaviorCount(userid, itemid, catid, behavior)
                if self.tag_date == self.pre_date:
                    self.extractPreUi(userid, itemid, behavior)
        self.uicRebuyRate()
        self.uicTransferCount()
        self.uicTransferRate()
        
    def secondReader(self):
        csv_list = self.windowReader._readFeatureSet()
        for day in range(self.time_window):
            for line in csv_list[day]:
                self.uiucCartNotBuy(line[0], line[1], line[4], day, line[2])

    def lastDayReader(self):
        csv_last_reader = self.windowReader._readTagSet()
        for line in csv_last_reader:
            self.extractTrainUi(line[0], line[1], line[2])

    ## combine features
    def uicCombine(self, dic_behaviorCount, dic_rebuyRate, dic_transferRate, key, uikey):
        for i in range(3):
            self.dic_allfeatures[uikey].extend(dic_behaviorCount[key][i])

        if key in dic_rebuyRate:
            self.dic_allfeatures[uikey].append(dic_rebuyRate[key])
        else:
            self.dic_allfeatures[uikey].append(0)

        if key in dic_transferRate:
            self.dic_allfeatures[uikey].extend(dic_transferRate[key])
        else:
            self.dic_allfeatures[uikey].extend([0,0,0])

    def uiucCombine(self, dic_behaviorCount, dic_cartNotBuy, k, key1, key2):
        if (key1, key2) in dic_behaviorCount:
            self.dic_allfeatures[k].extend(dic_behaviorCount[(key1, key2)])
        else:
            self.dic_allfeatures[k].extend([0,0,0,0])

        if (key1, key2) in dic_cartNotBuy:
            self.dic_allfeatures[k].extend(dic_cartNotBuy[(key1, key2)])
        else:
            self.dic_allfeatures[k].extend([0,0,0])

    def combineFeatures(self, dic_UI):
        for (k, v) in dic_UI.items():
            if k[0] in self.dic_uBehaviorCount and k[1] in self.dic_iBehaviorCount:    # the user and item should appear before the tag or pre day
                self.dic_allfeatures[k] = []
                
                self.uicCombine(self.dic_uBehaviorCount, self.dic_uRebuyRate, self.dic_uTransferRate, k[0], k)
                self.uicCombine(self.dic_iBehaviorCount, self.dic_iRebuyRate, self.dic_iTransferRate, k[1], k)
                self.uicCombine(self.dic_cBehaviorCount, self.dic_cRebuyRate, self.dic_cTransferRate, self.dic_item[k[1]][0], k)
                
                self.uiucCombine(self.dic_uiBehaviorCount, self.dic_uiCartNotBuy, k, k[0], k[1])
                self.uiucCombine(self.dic_ucBehaviorCount, self.dic_ucCartNotBuy, k, k[0], self.dic_item[k[1]][0])


    ## nomalize
    def nomalize(self):
        for (k, v) in self.dic_allfeatures.items():
            maxList = [0] * len(v)
            break

        for (k, v) in self.dic_allfeatures.items():
            for i in range(len(v)):
                if float(v[i]) > maxList[i]:
                    maxList[i] = float(v[i])
        print maxList

        for (k, v) in self.dic_allfeatures.items():
            self.dic_nomalfeatures[k] = []
            for i in range(len(v)):
                self.dic_nomalfeatures[k].append(float(v[i]) / maxList[i])

    def writeFeatureFile(self):
        if self.tag_date != self.pre_date:
            flag = 'train'
        else:
            flag = 'pre'
        if not os.path.isdir(self.output_dir + flag + os.sep):
            os.mkdir(self.output_dir + flag + os.sep)
        featureWriter = csv.writer(file(self.output_dir + flag + os.sep + self.tag_date + '.csv', 'wb'))
        for (k, v) in self.dic_nomalfeatures.items():
            if flag == 'train':
                line = [self.dic_train[k]]
            else:
                line = []
            line.extend(k)
            line.extend(self.dic_nomalfeatures[k])
            featureWriter.writerow(line)


    ## run all functions
    def _prepareFeatures(self):
        self.getItemDict()
        self.firstReader()
        self.secondReader()
        if self.tag_date != self.pre_date:
            self.lastDayReader()
            self.combineFeatures(self.dic_train)
        else:
            self.combineFeatures(self.dic_pre)
        self.nomalize()
        self.writeFeatureFile()

# test
a = extractFeaturesNTags('ori_data/', 'split_data/', 'features/', '2014-12-18', '2014-12-19', 3)
a._prepareFeatures()
print len(a.dic_uBehaviorCount)
print len(a.dic_uRebuyRate)
print len(a.dic_uTransferRate)
print len(a.dic_uiBehaviorCount)
print len(a.dic_uiCartNotBuy)
print len(a.dic_train)
print len(a.dic_allfeatures)
for (k, v) in a.dic_allfeatures.items():
    print len(v)
    break
