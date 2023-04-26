import sys
import os
from src import file

def change_input_file_name_nicely(filename):
    if '.' in filename:
        extension = filename.split('.')[-1]
        return filename.replace(f".{extension}", f"_calced.{extension}")
    return filename + "_calced"

inputFile = sys.argv[1]
if len(sys.argv) >= 3:
    outputFile = sys.argv[2]
else:
    outputFile = change_input_file_name_nicely(inputFile)

if os.path.isdir(inputFile):
    for filename in os.listdir(inputFile):
        output = change_input_file_name_nicely(filename)
        file.change_file(filename, output)
else:
    file.change_file(inputFile, outputFile)
