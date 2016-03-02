library(RSAGA)
filenames <- dir()[substring(dir(), nchar(dir())) == ".csv"]
grid = grid.to.xyz(as.matrix(read.csv('application_atom+xml_bfc_matrix.csv', header=FALSE)))
