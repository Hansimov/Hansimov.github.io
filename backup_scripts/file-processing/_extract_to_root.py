import os
import shutil

root = "./starname/"
fname_L = os.listdir(root)
for fname in fname_L:
    if os.path.isdir(root+fname):
        print(root+fname)
        for subfname in os.listdir(root+fname):
            name, ext = os.path.splitext(subfname)
            if ext in [".mp4", ".avi", ".mkv"]:
                old_subfname = os.path.join(root, fname, subfname)
                new_subfname = os.path.join(root, subfname)
                print("\t"+subfname)
                print("\t\t"+old_subfname)
                print("\t\t-> "+new_subfname)
                shutil.move(old_subfname, new_subfname)
