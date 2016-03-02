#!/usr/bin/evn python
#-------------------------------------------------------------------------------
# Name:_        BFA_hang
# Purpose:     Generate BFA signature for certain file type 
#
# Author:      Hang Guo
#
# Created:     2/19/2016
#-------------------------------------------------------------------------------

import sys, argparse,json

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--help", help="Sample input and output", action='store_true')
parser.add_argument("--debug", help="set 1 to turn on debugging mode", default=0) 
parser.add_argument("--MIME_type", help="mime type we're generateing output against", default="default_mime_type")
parser.add_argument("--file_list_path", help="the path for the file list of certain MIME Type", default="default_file_list") 
parser.add_argument("--output_file_name", help="output file name", default="default_out.signature")
args = parser.parse_args()

if args.help:
    print "This program takes in a file list containing full paths of certain type of files as argument and output an unified average byte frequency of all the file in file list"
    print "One sample row for the file list is: 160/201/178/155/C5402A255D63ED25FD81A0D9093C70B571D2FE2D3D0875BBA37AE674FD14D1EB"
    print "An example call to the scrtip: python BFA_hang.py --file_list_path ./test_list --output test_out_signature --MIME_type some_type which generate the byte freq signature test_out_signature.json and test_out_signature.text for file listed in test_list"
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

def get_byte_count_from_s3_path(s3_path):
	byte_count_list=[0]*256
	f = open(str(s3_path).strip(),'rb') #not sure what exactly file open conmmand is used for opening remote s3 file
                                            #rb means read in byte mode 
				            #strip() get rid of leading/trailing space -- hang
	byte=f.read(1)
	while byte != "":
		byte_count_list[ord(byte)]+=1
		byte=f.read(1)

#Function: convert a list containing averge byte occurance to a list containing byte freq
def average_byte_occurrence_to_byte_frequency(abolist):
	max_bl=max(abolist)
	abolist[:]=[x/max_bl*1.0 for x in abolist]
	return abolist

#Function: convert a byte freq list to a string of json format like shown below:
#[ { "name": "Application_Pdf",  "data":[ { "byte": 0, "bytefreq": 0.1 },{ "byte": 1, "bytefreq": 0.2}, {"byte": 2,"bytefreq": 0.3} ] } ]
#Input: bflist is byte freq list; typename is a string for the MIME type
#output: a json string
def bflist2json(bflist, typename):
	jsonstring="[ {  \"name\": \""+str(typename)+"\",  \"data\":[ "
        for i in range(256):
		datastring="{ \"byte\": "+str(i)+", \"bytefreq\": "+str(bflist[i])+" }"
		if i != 255:
			jsonstring=jsonstring+datastring+","
		else:
			jsonstring=jsonstring+datastring
	jsonstring=jsonstring+"] }   ]"
	return jsonstring	

def get_json_byte_frequency_string_from_filelist(file_list_path, MIME_type):
	flp=args.file_list_path
	average_byte_occurence_list=count_avg_byte_occurance(flp)#average_byte_occurence_list is a list containing average bype occurance
	byte_frequency_list=average_byte_occurrence_to_byte_frequency(average_byte_occurence_list) #byte_frequency_list is a list containing byte freq
	jsonstring=byte_frequency_list2json(byte_frequency_list,str(MIME_type))
	return(jsonstring)

get_json_byte_frequency_string_from_filelist(args.file_list_path, args.MIME_type)

#create a json file and save to it
out_fd_json=open(str(args.output_file_name)+".json",'w')
out_fd_json.write(str(jsonstring))
#create a txt file and save to it
out_fd_txt=open(str(args.output_file_name)+".txt",'w')
out_fd_txt.write("\n".join(map(str,byte_frequency_list)))
out_fd_json.close()
out_fd_txt.close()
if int(args.debug)==1:
	print "file_count="+str(file_count)+"\n"






























