import os
import shutil

root = "."
fname_L = os.listdir(root)
for fname in fname_L:
    if os.path.isdir(fname):
        print(fname)
        for subfname in os.listdir(fname):
            name, ext = os.path.splitext(subfname)
            if ext in [".mp4", ".avi", ".mkv", ".rmvb", ".wmv"]:
                old_subfname = os.path.join(root, fname, subfname)
                new_subfname = os.path.join(root, subfname)
                print(subfname)
                shutil.move(old_subfname, new_subfname)