import sys
from _rename_folder_batch import *

for folder in sys.argv[1:]:
    # print(folder)
    renameFolder(folder)
    # os.system("pause")