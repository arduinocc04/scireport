import sys
import os
from scicalc.src import file

def change_input_file_name_nicely(filename:str) -> str:
    """append _calced at filename without extension.

    Args:
        filename: a string(filename)

    Returns:
        a string.
    """
    if '.' in filename:
        extension = filename.split('.')[-1]
        return filename.replace(f".{extension}", f"_calced.{extension}")
    return filename + "_calced"

input_file = sys.argv[1]
if len(sys.argv) >= 3:
    outputFile = sys.argv[2]
else:
    outputFile = change_input_file_name_nicely(input_file)

if os.path.isdir(input_file):
    for filename in os.listdir(input_file):
        output = change_input_file_name_nicely(filename)
        file.change_and_execute_file(filename, output, "@@")
else:
    file.change_and_execute_file(input_file, outputFile, "@@")
