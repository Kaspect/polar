#!/usr/bin/evn python
#-------------------------------------------------------------------------------
# Name:        BFA_hang
# Purpose:     Generate BFA signature for certain file type 
#
# Author:      Hang Guo
#
# Created:     2/19/2016
#-------------------------------------------------------------------------------

import sys, argparse

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--help", help="Sample input and output", action='store_true')
parser.add_argument("--debug", help="set 1 to turn on debugging mode", default=0) 
parser.add_argument("--file_list_path", help="the path for the file list of certain MIME Type", default="default_file_list") 
parser.add_argument("--output_file_name", help="output file name", default="default_out.signature")
args = parser.parse_args()

if args.help:
    print "This program takes in a file list containing full paths of certain type of files as argument and output an unified average byte frequency of all the file in file list"
    print "One sample row for the file list is: 160/201/178/155/C5402A255D63ED25FD81A0D9093C70B571D2FE2D3D0875BBA37AE674FD14D1EB"
    print "An example call to the scrtip: python BFA_hang.py --file_list_path ./test_list --output test_out.signature which generate the byte freq signature test_out.signature for file listed in test_list"
    sys.exit()

#Function:Count the avarge occurance of byte 0~255 in all the files contained in the inputted list 
#	  Average_occunrace=total_occurance/file_count
#Input:Full path of a list containing all data files of certain MIME type
#Output:256 element python list containing the average occurance count of byte 0~255 in those files (occurance of byte x can be retrived as list[x])
def count_avg_byte_occurance(file_list_path):
	file_list_fd=open(file_list_path,'r')
	file_count=0
	abolist=[0]*256	
	for line in file_list_fd:
        	try:
                	if int(args.debug)==1:
                        	print "Current line in file list="+str(line)+"\n"
                	f = open(str(line).strip(),'rb')
                	byte=f.read(1)
                	while byte != "":
                        	abolist[ord(byte)]+=1
                        	byte=f.read(1)
        	except:
                	print "Failed to finish parsing file "+str(line)+"\n"
                	f.close()
                	continue
        	file_count+=1
        	f.close()
	abolist[:]=[x/file_count*1.0 for x in abolist]
	file_list_fd.close()
	return abolist

#Function: convert a list containing averge byte occurance to a list containing byte freq
def abo2bf(abolist):
	max_bl=max(abolist)
	abolist[:]=[x/max_bl*1.0 for x in abolist]
	return abolist

	 
flp=args.file_list_path
out_fd=open(str(args.output_file_name),'w')
abolist=count_avg_byte_occurance(flp)#abolist is a list containing average bype occurance
bflist=abo2bf(abolist) #bflist is a list containing byte freq
out_fd.write("\n".join(map(str,bflist)))
out_fd.close()
if int(args.debug)==1:
	print "file_count="+str(file_count)+"\n"
