def initialize(fingerprint):
    for i in range(0,256):
        fingerprint[i] = 0
    return fingerprint

# calculates the correlation for one file using old_fingerprint
# old_fingerprint : finger print of the mime type calculated from the training set data from BFA
# new_fingerprint : byte map of the test data from BFA
# returns the correlation computed from both parameters
def calculateCorelationFactor(old_fingerprint, new_fingerprint):
    corelation = {}
    for i in range(0,256):
        corelation[i] = 0
    sigma = 0.0375
    for i in range(0,256):
        x = new_fingerprint[i] - old_fingerprint[i]
        corelation[i] = math.exp(-1*(math.pow(x,2))/(2*(math.pow(sigma,2))))
    return corelation

#Update Correlation
def updateCorelation(corelation,corelation1,file_count):
    for i in range(0,256):
        corelation1[i] = (corelation1[i]*file_count +corelation[i])/(file_count+1)
    return

#Update Fingerprint
def updateFingerprint(old_fingerprint, fingerprint,file_count):
    for i in range(0,256):
        fingerprint[i] = (fingerprint[i]*file_count + old_fingerprint[i])/(file_count+1)
    return

def readFile(location):
    list = [0]
    byteList = list*256
    with open(location,'rb') as file:
        bytes = file.read(1)
        while bytes != "":
            bytes = file.read(1)
            if len(bytes) > 0:
                byteList[ord(bytes)] += 1
        file.close()
    return byteList

# fingerprint : fingerprint of the mime type
# listFiles : list of file locations to compute the correlation
# returns the corelation of the mime type
def getBFD(fingerprint, listFiles):
    corelation = {}
    corelation = initialize(corelation)

    filecount = 0
    for file in listFiles:
        bytemap = readFile(file)
        file_correlation = calculateCorelationFactor(fingerprint, bytemap)
        updateCorelation(file_correlation, corelation, filecount)
        filecount += 1
    return correlation
