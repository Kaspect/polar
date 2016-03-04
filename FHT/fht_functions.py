#TODO implement the matrix generation for the footer work.
#TODO run on the whole dataset.

import sys, argparse, json
import os

import numpy as np
import matplotlib.pyplot as plt
# http://stackoverflow.com/questions/1035340/reading-binary-file-in-python-and-looping-over-each-byte
#Function:Count the avarge occurance of byt
		
def test_file_list():
		return(["test_img_files/IMG_1295.jpg",
				"test_img_files/IMG_1296.jpg",
				"test_img_files/IMG_1297.jpg",
				"test_img_files/IMG_1304.jpg",
				"test_img_files/IMG_1305.jpg",
				"test_img_files/IMG_1306.jpg",
				"test_img_files/IMG_1307.jpg",
				"test_img_files/IMG_1308.jpg",
				"test_img_files/IMG_1309.jpg",
				"test_img_files/IMG_1310.jpg",
				"test_img_files/IMG_1311.jpg",
				"test_img_files/IMG_1312.jpg",
				"test_img_files/IMG_1313.jpg",
				"test_img_files/one_byte.jpg",
				"test_img_files/five_bytes.jpg",
				"test_img_files/nine_bytes.jpg",
				"test_img_files/eighteen_bytes.jpg"]
				)
def read_file_list(file_list_path="default_file_list"):
	list = [str(x).rstrip('\n') for x in open(file_list_path,'r')]
	return(list)

def gen_expected_distribution_for_one_byte_b():
	neg1_list = np.ones(256)*-1
	mat = np.vstack([np.zeros(256), neg1_list,neg1_list,neg1_list])
	mat[0,98] = 1
	return(mat)
def gen_expected_matrix_for_two_short_files():
	neghalflist = np.ones(256)*-0.5
	mat = np.vstack([np.zeros(256), neghalflist,neghalflist,neghalflist])
	return(mat)

def bytes_from_file(filename, chunksize, num_bytes_to_collect,is_trailer):
	with open(filename, "rb") as f:
		while True:
			if is_trailer:
				#set the position to be read backwards
				index_near_end = -1 * num_bytes_to_collect
				f.seek(index_near_end,2)
			chunk = f.read(chunksize)
			if chunk:
				for b in chunk:
					yield b
			else:
				break

def bytes(filename, num_bytes_to_collect, is_trailer):
	L = []
	bytes_recorded_so_far=0
	for b in bytes_from_file(filename, 8192,num_bytes_to_collect, is_trailer):
		L += [b]
		bytes_recorded_so_far += 1
		if bytes_recorded_so_far == num_bytes_to_collect:
			break
	return(L)

#returns just an integer of the num bytes in a file
def get_length_of_file_in_bytes(filename):
	return(os.path.getsize(filename))

# def bytes_backwards(filename, num_bytes_to_collect):
# 	with open(filename, "rb") as f:
# 		f.seek(num_bytes_to_collect, 2)
# 	return(testdata)


def extract_first_n_elements(n, L):
	return(L[0:n])

def extract_n_header_bytes_from_file(filename, number_of_bytes):
	header_bytes = bytes(filename, number_of_bytes, 0)
	return(header_bytes)

def extract_n_footer_bytes_from_file(filename, number_of_bytes):
	footer_bytes = bytes(filename, number_of_bytes, 1) #Reverse the bytes so we can reuse the 
	return(footer_bytes)

def zero_matrix_for_FHT(first_n_bytes):
	return(np.zeros((first_n_bytes, 256), dtype=int))

def build_FHT_header_matrix(filename, first_n_bytes):
	#Instantiated the matrix of zeros
	header_matrix =  zero_matrix_for_FHT(first_n_bytes)
	#Grab the file header bytes
	file_header_bytes = extract_n_header_bytes_from_file(filename,first_n_bytes)
	counter = 0
	for byte_value in file_header_bytes:
		header_matrix[counter,byte_value] = 1
		counter += 1
	header_matrix = plug_in_negative_numbers_if_file_is_shorter_than_header_len(filename, first_n_bytes, header_matrix)
	return(header_matrix)

def build_FHT_footer_matrix(filename, last_n_bytes):
	#Instantiated the matrix of zeros
	footer_matrix =  zero_matrix_for_FHT(last_n_bytes)
	#Grab the file header bytes
	file_footer_bytes = extract_n_footer_bytes_from_file(filename,last_n_bytes)
	counter = 0
	for byte_value in file_footer_bytes:
		footer_matrix[counter,byte_value] = 1
		counter += 1
	footer_matrix = plug_in_negative_numbers_if_file_is_shorter_than_header_len(filename, last_n_bytes, footer_matrix)
	return(footer_matrix)	

def plug_in_negative_numbers_if_file_is_shorter_than_header_len(filename,first_n_bytes,header_matrix):
	if get_length_of_file_in_bytes(filename) >= first_n_bytes:
		return(header_matrix)
	else:
		index_of_last_bit_position_in_file = get_length_of_file_in_bytes(filename)
		for i in range(index_of_last_bit_position_in_file, first_n_bytes):
			header_matrix[i] = np.ones(256)*-1
		return(header_matrix)

# def concatenate_FHT_matrices(matrix1, matrix2):

# This is the same for header and footer
def concatenate_FP_matrices(old_FP_matrix, new_FP_matrix, previous_number_of_files):
	weighted_matrix_sum = old_FP_matrix*previous_number_of_files + new_FP_matrix
	new_sample_size = previous_number_of_files + 1
	concatenated_matrix = weighted_matrix_sum/new_sample_size
	return(concatenated_matrix)


def concatenate_FP_matrix_from_filelist(filelist, num_bytes=8, header_or_footer="NULL"):
	# Instantiate the matrix for the initial FHT Matrix
	variable_matrix = zero_matrix_for_FHT(num_bytes)
	previous_number_of_files = 0
	for file in filelist:
		if header_or_footer=="header":
			current_file_matrix = build_FHT_header_matrix(file,num_bytes)
		else:
			current_file_matrix = build_FHT_footer_matrix(file, num_bytes)
		variable_matrix = concatenate_FP_matrices(variable_matrix, current_file_matrix, previous_number_of_files)
		previous_number_of_files += 1
		print('files_remaining = ' + str(len(filelist) - previous_number_of_files))
	return(variable_matrix)

##################################
#Testing Framework
##################################


import unittest
 
class TestUM(unittest.TestCase):
 
	def setUp(self):
		pass

	def test_build_FHT_header_matrix_size_is_correct(self):
		self.assertEqual(build_FHT_header_matrix("test_img_files/IMG_1305.jpg",4).shape, (4, 256))
		self.assertEqual(build_FHT_header_matrix("test_img_files/IMG_1305.jpg",8).shape, (8, 256))
		self.assertEqual(build_FHT_header_matrix("test_img_files/IMG_1305.jpg",16).shape, (16, 256))


	def test_concatenate_FP_matrices(self):
		building_pic_matrix = build_FHT_header_matrix("test_img_files/IMG_1305.jpg",4)
		stairs_pic_matrix = build_FHT_header_matrix("test_img_files/IMG_1307.jpg",4)
		# I start the previous number files at one because there 
		# were no images before I added the building pic
		concatenated_matrix = concatenate_FP_matrices(building_pic_matrix, stairs_pic_matrix, 1)
		np.testing.assert_array_equal(concatenated_matrix, building_pic_matrix)


	def test_concatenate_FP_matrices_for_short_ones_for_errors(self):
		just_the_letter_b_jpg_matrix = build_FHT_header_matrix("test_img_files/one_byte.jpg",4)
		np.testing.assert_array_equal(just_the_letter_b_jpg_matrix, gen_expected_distribution_for_one_byte_b())
		brian_jpg_matrix = build_FHT_header_matrix("test_img_files/five_bytes.jpg",4)
		# I start the previous number files at one because there 
		# were no images before I added the building pic
		concatenated_matrix = concatenate_FP_matrices(just_the_letter_b_jpg_matrix, brian_jpg_matrix, 1)
		return(concatenated_matrix)

	def test_concatenate_FP_matrix_from_filelist(self):
		res1 = concatenate_FP_matrix_from_filelist(test_file_list(), 4, header_or_footer="header")
		return(res1)


def run_header_and_footer(type_name, list_of_filenames, bytes_to_check):
	#prep filenames
	header_FHT_filename_out = type_name + "_header_FHT"
	footer_FHT_filename_out = type_name + "_footer_FHT"
	# Generate output files into those filenames
	# One for header and one for trailer
	save_csv_for_each_byte_len(list_of_filenames, filename_out = header_FHT_filename_out, bytes_to_check=bytes_to_check, header_or_footer="header")
	# save_csv_for_each_byte_len(list_of_filenames, filename_out = footer_FHT_filename_out, bytes_to_check=bytes_to_check, header_or_footer="footer")


def save_csv_for_each_byte_len(list_of_filenames, filename_out, bytes_to_check, header_or_footer):
	for i in bytes_to_check:
		filename_with_bytes = filename_out + "bytelen" + str(i) + ".csv"
		print("Working on: " + filename_with_bytes)
		mat = concatenate_FP_matrix_from_filelist(list_of_filenames, i, header_or_footer)
		np.savetxt(filename_with_bytes, mat, delimiter=",")
 

def read_first_n_bytes(filename, num_bytes):
	file = open(filename, 'rb')
	# while 1:
	byte = file.read(num_bytes)
	return byte


if __name__ == '__main__':
	# unittest.main()
	print('Unit tests complete')
	#replace test_file_list with a list of the files. strings
	run_header_and_footer("jpg", test_file_list(), bytes_to_check = [4,8,16] )
	# run_header_and_footer("filename_for_group_of_files", read_file_list("path_to_list_of_files"), bytes_to_check = [4,8,16] )
