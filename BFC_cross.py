#!/usr/bin/evn python
#-------------------------------------------------------------------------------
# Name:_        BFC_cross
# Purpose:     Generate BFC cross correlation matrix for 15 MIME type we chose
#	       The matrix countain the following info: 
#	        -Dignoals: number of files that have been used to compute the fingerprint
#		- (i,j) store the difference in byte occurnace
#		- (j,i) store the normalized value
# Author:      Hang Guo
#
# Created:     2/19/2016
#-------------------------------------------------------------------------------

import sys, argparse,csv

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--help", help="Sample input and output", action='store_true')
parser.add_argument("--debug", help="set 1 to turn on debugging mode", default=0)
parser.add_argument("--textual_byte_occurance", help="path for the textual format byte occurnace count", default="default_signature.abolist")
parser.add_argument("--file_number", help="file number used to calculate the signature", default="1000")
parser.add_argument("--output_file_name", help="output file name", default="default_bfc_matrix.csv")
args = parser.parse_args()

if args.help:
    print "This program takes in a textual format signature and output a bfc matrix in comma separated format"
    print "An example call to the scrtip: python BFC_cross.py --textual_byte_occurance default_signature.abolist --output_file_name default_bfc_matrix.csv --file_number 1000" 
    sys.exit()

#Add file number to the diagnoal of the bfc_matrix
def add_dia(file_number,mx):
	for i in range(256):
		mx[i][i]=file_number
	return mx
#load byte occurance count from text file into a python list
def text2list(text_path):
	text_fd=open(str(text_path),'r')
	abolist=[]
	for line in text_fd:
		abolist.append(float(line))
	text_fd.close()
	if int(args.debug)==1:
		print "abolist+"+str(abolist)
	return abolist

#add (i,j), the difference in byte occurnace (byte_occurance_i - byte_occurance_j)
#add (j,j), the normalized value
def add_rest(mx,abolist):
	max_diff=0
	for i in range(256):
		for j in range(i+1,256):
			mx[i][j]=abs(abolist[i]-abolist[j])
			if mx[i][j]>max_diff:
				max_diff=mx[i][j]
	if int(args.debug)==1:
		print "max_diff="+str(max_diff)

	for i in range(1,256):
		for j in range(0,i):
			mx[i][j]=float(mx[j][i])/max_diff*1.0
	return mx	

file_num=int(args.file_number)
out_fn=str(args.output_file_name)
bfc_matrix_0=[[0 for x in range(256)] for x in range(256)]
bfc_matrix_1=add_dia(file_num,bfc_matrix_0)
abolist=text2list(str(args.textual_byte_occurance))
bfc_matrix_2=add_rest(bfc_matrix_1, abolist)

with open(out_fn, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(bfc_matrix_2)



