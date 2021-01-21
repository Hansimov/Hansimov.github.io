import sys
from _resize_img_batch import *

for imgname in sys.argv[1:]:
    resizeThis(imgname)
