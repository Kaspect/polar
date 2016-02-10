def main():
  polar_data = download_s3_data_from_polar()
  byte_frequency_analysis(one_file_path)
  byte_frequency_distribution_correlation()
  byte_frequency_cross_correlation()
  file_header_trailer()
  produce_json_output_for_d3()
  produce_json_output_for_pie_chart()
  run_tika_simularity(polar_data, distances=['jaccard','cosine','edit_similarity'])
  run_content_based_mime_detector(polar_data)

  

