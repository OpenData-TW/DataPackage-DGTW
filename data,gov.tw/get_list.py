from os import listdir
from os.path import isfile, join

mypath = '.'

dir_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

