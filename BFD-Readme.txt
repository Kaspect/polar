Consider the method getBFD() in the file BFD.py

The method needs 2 parameters:
1. fingerprint : the computed finger print of the mime type from BFA. (from training data)
2. list of files locations : the list of files for computing the correlation (using testing data)

The method would return the correlation array.

For visualization:
1. fingerprint as an array
2. the correlation array

These two arrays would be passed to the D3.js to create the visualization.
