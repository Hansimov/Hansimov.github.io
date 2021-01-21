import sys
from _short2long_batch import *

imgnames = []
for imgname in sys.argv[1:]:
    imgnames.append(imgname)

short2long(imgnames)