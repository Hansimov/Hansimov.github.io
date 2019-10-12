import os
import re

magick = "D:/ImageMagick/magick.exe convert "

CROP_HEIGHT = 50
CROP_OFF_Y = 445
CHOP_HEIGHT = 25
IS_CROP_FIRST = False
SHARPEN = 4
# BLACK_THRESHOLD = 0

def sortImgs(imgInames):
    nameexts = []
    for imgIname in imgInames:
        name,ext = os.path.splitext(imgIname)
        nameexts.append([name,ext])
    nameexts = sorted(nameexts,key=lambda l:l[0], reverse=False)
    sortedimgInames = []
    for nameext in nameexts:
        sortedimgInames.append(nameext[0]+nameext[1])
    return sortedimgInames

cmd_crop = magick + " \"{}\" -crop 0x{}+0+{} \"{}\""
cmd_chop = magick + " \"{}\" -gravity South -chop 0x{} \"{}\""
def cropImg(imgIname, isBegin=False, totalNum=0):
    name,ext = os.path.splitext(imgIname)
    imgCname = name+"_crop"+ext
    if not isBegin:
        os.system(cmd_crop.format(imgIname,CROP_HEIGHT,CROP_OFF_Y, imgCname))
    else:
        if totalNum == 1:
            os.system(cmd_chop.format(imgIname, 0, imgCname))
        else:
            os.system(cmd_chop.format(imgIname, CHOP_HEIGHT, imgCname))
    return imgCname

def concatImgNames(imgInames):
    imglongstr = ""
    for imgIname in imgInames:
        imglongstr += " \"{}\" ".format(imgIname)
    return imglongstr

cmd_combine = magick + " -adaptive-sharpen 0x{} -append {} \"{}\""
def combineCroppedImgs(imgCnames):
    imgClongstr = concatImgNames(imgCnames)
    imgLname, imgLext = os.path.splitext(imgCnames[-1])

    imgLname = imgLname.replace("_crop", "")
    imgLname = imgLname + "_囗囗囗_{}".format(len(imgCnames)) + imgLext
    print("{} imgs combined.".format(len(imgCnames)))
    os.system(cmd_combine.format(SHARPEN,imgClongstr, imgLname))
    return imgLname

def short2long(imgInames):
    imgInames = sortImgs(imgInames)
    imgCnames = []

    for i in range(len(imgInames)):
        imgCname = cropImg(imgInames[i],i==0,len(imgInames))
        imgCnames.append(imgCname)

    combineCroppedImgs(imgCnames)

    for i in range(0, len(imgInames)):
        os.remove(imgCnames[i])

cmd_combine_no_crop = magick + " -append {} \"{}\""
def xshort2long(imgInames):
    imgInames = sortImgs(imgInames)
    imgIlongstr = concatImgNames(imgInames)
    imgLname, imgLext = os.path.splitext(imgInames[-1])

    imgLname = re.sub(r"_囗囗囗_\d+", "", imgLname)
    imgLname = imgLname + "_𪚥𪚥𪚥_{}".format(len(imgInames)) + imgLext
    print("{} imgs combined.".format(len(imgInames)))
    os.system(cmd_combine_no_crop.format(imgIlongstr,imgLname))

if __name__ == '__main__':
    pass
    imgInames = [
        "z1.jpg",
        "z2.jpg"
    ]
    xshort2long(imgInames)