import os
import math

def renameFolder(folder):
    filenames = os.listdir(folder)
    digits = math.ceil(math.log(len(filenames)+1,10))
    idx = 0
    for filename in filenames:
        _ , ext = os.path.splitext(filename)
        if not ext in [".jpg",".jpeg",".png",".bmp",".gif"]:
            continue
        idx += 1
        foldersuffix = os.path.split(folder)[-1]

        src = (folder+"\\"+filename).replace("\\","/")
        tgt = ("{}\\{}-{:0>{digits}}{}".format(folder,foldersuffix,idx,ext,digits=digits)).replace("\\","/")
        cmd_rename_folder = (src,tgt)
        # print(cmd_rename_folder)
        os.rename(src,tgt)

if __name__ == '__main__':
    folder = "0013"
    renameFolder(folder)