import sys
from _anti_weibo_batch import *

for imgname in sys.argv[1:]:
    antiWB(imgname)

# os.system("pause")