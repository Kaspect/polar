http://stackoverflow.com/questions/1035340/reading-binary-file-in-python-and-looping-over-each-byte
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
for b in bytes_from_file('samplefile.txt'):
    print(b)