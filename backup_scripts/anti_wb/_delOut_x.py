import sys
import os
sys.path.append('D:/_hanslab/backup_scripts/anti_wb/')

from _delOut import *

if __name__ == '__main__':
    for imgname in os.listdir(home):
        # print(imgname)
        delelteOut(imgname)