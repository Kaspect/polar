def main():
  polar_data = download_s3_data_from_polar()
  file_freq = byte_frequency_analysis(one_file_path)
  byte_frequency_distribution_correlation()
  byte_frequency_cross_correlation()
  file_header_trailer()
  produce_json_output_for_d3()
  produce_json_output_for_pie_chart()
  run_tika_simularity(polar_data, distances=['jaccard','cosine','edit_similarity'])
  run_content_based_mime_detector(polar_data)

#@param path_to_file some file that we want a byte frequency analysis of
#@return fingerprint 2D dataset with columns 'byte_length' and 'count'
#finger print will be in this format: pandas.DataFrame([0, 1,2,3,4,5], [43,26,33,25,32,1])
def byte_frequency_analysis(path_to_file):
  return 0

#@param path_to_file some file that we want a byte frequency correlations of
#@param fingerprint_array list of fingerprints, each with an identifier (see byte_frequency_cross_correlation)
#@return ???????????????? 
def byte_frequency_distribution_correlation(path_to_file,fingerprint_array):
    return 0


#@param path_to_file some file that we want a byte frequency correlations of
#@param fingerprint_array list of fingerprints, each with an identifier
#in this format:
#[
#    ('type1', pandas.DataFrame([0, 1,2,3,4,5], [43,26,33,25,32,1])),
#    ('type2', pandas.DataFrame([0, 1,2,3,4,5], [43,26,33,25,32,1])),
#    ('type3', pandas.DataFrame([0, 1,2,3,4,5], [43,26,33,25,32,1]))
#    ]
#@return ???????????????? 
def byte_frequency_cross_correlation(path_to_file,fingerprint_array):
      return 0
#@param path_to_file string path to the file for analysis
#@param bytes_to_analyze either 4,8,or 16 as an integer, indicating how many of the first bytes we should analyze
#@return sparse densematrix of what?????????????
def file_header_trailer(path_to_file,bytes_to_analyze):
  return 0


