import sys
import math

def discrete_feature( input_file_name, output_file_name,
                      seperator, col_num, discrete_num,
                      except_list=() ):
    infile = open(input_file_name,'r')
    # init
    feature_lists = []
    slice_boundary = []
    for i in range(col_num):
        feature_lists.append([])
        slice_boundary.append([])
    count = 0
    output_file = open(output_file_name,'w+')
    # read file
    for line in infile:
        record = line.split(seperator)
        if len(record) != col_num:
            print line
        else:
            count += 1
            for i in range(len(record)):
                if i not in except_list:
                    feature_lists[i].append(float(record[i]))
    # slice
    slice_length = int(math.ceil(1.0*count/discrete_num))

    # sort
    for f_list in feature_lists:
        f_list.sort()

    # set boundary
    for i in range(len(feature_lists)):
        if i in except_list:
            continue
        slice_boundary[i].append(feature_lists[i][slice_length-1])
        j = 1
        while( slice_length*j < count ):
            if (feature_lists[i][slice_length*j-1]) != slice_boundary[i][-1]:
                slice_boundary[i].append( feature_lists[i][slice_length*j-1] )
            j += 1
    print 'slice_boundary',slice_boundary
    # discrete
    infile.seek(0)
    for line in infile:
        record = line.split(seperator)
        discrete_record = []
        if len(record) != col_num:
            print line
        else:
            for i in range(len(record)):
                if i in except_list:
                    discrete_record.append(record[i])
                else:
                    tmp = ['0']*(len(slice_boundary[i])+1)
                    print 'tmp',tmp
                    for j in range(len(slice_boundary[i])):
                        print float(record[i]), slice_boundary[i][j]
                        if float(record[i]) <= slice_boundary[i][j]:
                            tmp[j] = '1'
                            break
                        if j == len(slice_boundary[i])-1:
                            tmp[j+1] = '1'
                            break
                    print tmp
                    discrete_record += tmp
        print discrete_record
        output_file.write(seperator.join(discrete_record)+'\n')
    output_file.flush()
    output_file.close()

# if __name__ == '__main__':
#     if len(sys.argv) != 7 or len(sys.argv) != 6:
#         print '''
#     error input parameters! expected 6 parameters, given %s
#     usage: python discrete_feature.py input_file output_file seperator col_num discrete_num [except_list]
#         except_list use ',' to seperate
#     ''' % (len(sys.argv)-1)
#         sys.exit(-1)
#     elif len(sys.argv) == 7:
#         discrete_feature(sys.argv[1], sys.argv[2], sys.argv[3],
#                      sys.argv[4], sys.argv[5], sys.argv[6].split(','))
#     elif len(sys.argv) == 6:
#         discrete_feature(sys.argv[1], sys.argv[2], sys.argv[3],
#                      sys.argv[4], sys.argv[5])

# test
# discrete_feature('d:/gsh/test_discrete', 'd:/gsh/test_discrete_out', ',',
#                       3, 5, (0,))
