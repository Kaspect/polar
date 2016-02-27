import ipdb
import numpy as np
import matplotlib.pyplot as plt
# http://stackoverflow.com/questions/1035340/reading-binary-file-in-python-and-looping-over-each-byte

        
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
                "test_img_files/IMG_1313.jpg"]
                )

def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break

# example:
def bytes(filename):
	L = []
	for b in bytes_from_file(filename):
	    L += [b]
	return(L)
	

def fht_main():
	return(bytes('samplefile.txt'))

def extract_first_n_elements(n, L):
    return(L[0:n])

def extract_n_header_bytes_from_file(filename, number_of_bytes):
    header_bytes = extract_first_n_elements(number_of_bytes, bytes(filename))
    return(header_bytes)

def extract_n_footer_bytes_from_file(filename, number_of_bytes):
    reversed_bytes = bytes(filename)[::-1] #Reverse the bytes so we can reuse the 
    footer_bytes = extract_first_n_elements(number_of_bytes, reversed_bytes)
    return(footer_bytes)

def n_byte_headers_for_each_file(list_of_filenames, number_of_bytes):
    header_byte_list = [extract_n_header_bytes_from_file(filename, number_of_bytes) for filename in list_of_filenames]
    return(header_byte_list)

def n_byte_footers_for_each_file(list_of_filenames, number_of_bytes):
    footer_byte_list = [extract_n_footer_bytes_from_file(filename, number_of_bytes) for filename in list_of_filenames]
    return(footer_byte_list)

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
    return(header_matrix)


# def concatenate_FHT_matrices(matrix1, matrix2):

# This is the same for header and footer
def concatenate_FP_matrices(old_FP_matrix, new_FP_matrix, previous_number_of_files):
    weighted_matrix_sum = old_FP_matrix*previous_number_of_files + new_FP_matrix
    new_sample_size = previous_number_of_files + 1
    concatenated_matrix = weighted_matrix_sum/new_sample_size
    return(concatenated_matrix)


def concatentate_FP_matrix_from_filelist(filelist, num_bytes=8):
    # Instantiate the matrix for the initial FHT Matrix
    variable_matrix = zero_matrix_for_FHT(num_bytes)
    previous_number_of_files = 0
    for file in filelist:
        current_file_matrix = build_FHT_header_matrix(file,num_bytes)
        variable_matrix = concatenate_FP_matrices(variable_matrix, current_file_matrix, previous_number_of_files)
        previous_number_of_files += 1
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

    def test_concatentate_FP_matrix_from_filelist(self):
        res1 = concatentate_FP_matrix_from_filelist(test_file_list(), 4)
 
    # def test_strings_a_3(self):
    #     self.assertEqual( multiply('a',3), 'aaa')
 
if __name__ == '__main__':
    unittest.main()