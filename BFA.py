import os

def changeToPresentDirectory():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

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

changeToPresentDirectory()

os.chdir(os.getcwd())

byteValue = 0
with open('byteCount.tsv','w') as fileOutput:
    fileOutput.write('Byte     Frequency\n' )
    for frequency in readFile("/Users/dhruvbhatia/Desktop/Dhruv_Resume.pdf"):
        fileOutput.write('Byte '+str(byteValue) + ' : ' + str(frequency)+'\n')
        byteValue +=1
