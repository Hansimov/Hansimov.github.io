import sys
from _combine_img_batch import *

imgnames = []
for imgname in sys.argv[1:]:
    imgnames.append(imgname)

appendImg(imgnames)
