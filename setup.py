import os

try:
    os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), "misc"))
    os.mkdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), "log"))
except:
    pass

os.system("echo ")