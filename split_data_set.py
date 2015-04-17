#coding:utf-8

__author__ = 'luolan.ll'
import sys

def split_data( input_file_name, output_dir, bad_record_file_name):
    infile = open(input_file_name,'r')
    bad_record_file = open(bad_record_file_name,'w+')
    outfile_dict ={}
    infile.readline()
    for line in infile:
        if len(line.split(',')) != 6:
            print line
            bad_record_file.write(line)
        else:
            output_file_name = output_dir + '/' + line.strip().split(',')[-1].split(' ')[0]
            if not outfile_dict.has_key(output_file_name):
                outfile_dict[output_file_name] = open(output_file_name,'w+')
            outfile_dict[output_file_name].write(line)

    bad_record_file.flush()
    bad_record_file.close()
    for key in outfile_dict:
        outfile_dict[key].flush()
        outfile_dict[key].close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '''
        error input parameters! expected 3 parameters, given %s
        usage: split_data_set.py input_file_name output_dir bad_record_file_name
        ''' % (len(sys.argv)-1)
        sys.exit(-1)
    split_data(sys.argv[1], sys.argv[2], sys.argv[3])