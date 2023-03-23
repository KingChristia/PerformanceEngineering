import sys
import re

def ImportChessDataBase(filePath, counts):
    inputFile = open(filePath, "r")
    count = ReadChessDataBase(inputFile, counts)
    inputFile.close()

def ReadChessDataBase(inputFile, counts):
    count = 0
    for line in inputFile:
        line = line.rstrip() # remove the end of the line character
        if re.search("Result", line):
            if re.search("1-0", line):
                counts[0] = counts[0] + 1
            elif re.search("0-1", line):
                counts[1] = counts[1] + 1
            else:
                counts[2] = counts[2] + 1

counts = [0, 0, 0]
ImportChessDataBase("DataBases/Stockfish_15_64-bit.commented.[2600].pgn", counts)
print(counts)