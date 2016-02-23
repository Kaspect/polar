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
    print "An example call to the scrtip it: python BFA_hang.py --file_list_path ./test_list --output test_out.signature which generate the byte freq signature test_out.signature for file listed in test_list"
    sys.exit()

flp=args.file_list_path
file_list_fd=open(flp,'r')
out_fd=open(str(args.output_file_name),'w')
file_count=0
bytelist=[0]*256

for line in file_list_fd:
	try:
		if int(args.debug)==1:
			print "Current line in file list="+str(line)+"\n"
		f = open(str(line).strip(),'rb')
		byte=f.read(1)
		while byte != "":
			bytelist[ord(byte)]+=1
			byte=f.read(1)
	except:
		print "Failed to finish parsing file "+str(line)+"\n"
		f.close()
		continue
	file_count+=1
	f.close()

bytelist[:]=[x/file_count*1.0 for x in bytelist]
max_bl=max(bytelist)
bytelist[:]=[x/max_bl*1.0 for x in bytelist]
out_fd.write("\n".join(map(str,bytelist)))

if int(args.debug)==1:
	print "file_count="+str(file_count)+"\n"
	print "max in bytelist="+str(bytelist)+"\n"
file_list_fd.close()
out_fd.close()
