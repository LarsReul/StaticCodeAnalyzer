import ast
import sys
import os
import tryStuff
import re

directory = sys.argv[1]

filePaths = tryStuff.getFilesWithEndingFromDirectory(directory, ".py")

for filePath in filePaths:
    lineCount = 0
    emptyLineCount = 0
    if filePath.endswith("tests.py"):
        continue

    file = open(filePath)

    for line in file:
        lineCount += 1

        tryStuff.checkLineOfFile(filePath, line, lineCount)

        if line.strip() == "":
            emptyLineCount += 1
        else:
            if emptyLineCount >2:
                print(f"{filePath}: line {lineCount}: S006 More than two blank lines used before this line")
            emptyLineCount = 0

        tryStuff.checkLineOfFile2(filePath, line, lineCount)

    tryStuff.check010(filePath)