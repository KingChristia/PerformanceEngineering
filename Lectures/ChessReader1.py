import sys
import re

def ImportChessDataBase(filePath):
    inputFile = open(filePath, "r")
    count = ReadChessDataBase(inputFile)
    inputFile.close()
    return count

def ReadChessDataBase(inputFile):
    count = 0
    for line in inputFile:
        line = line.rstrip() # remove the end of the line character
        if re.search("Event", line):
            count = count + 1
    return count

count = ImportChessDataBase("DataBases/Stockfish_15_64-bit.commented.[2600].pgn")
print(count)