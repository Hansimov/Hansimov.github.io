import os

magick = "D:/ImageMagick/magick.exe convert "

CROP_HEIGHT = 50
CROP_OFF_Y = 445
CHOP_HEIGHT = 25
IS_CROP_FIRST = False
SHARPEN = 8
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
def cropImg(imgIname, isBegin=False):
    name,ext = os.path.splitext(imgIname)
    imgCname = name+"_crop"+ext
    if not isBegin:
        os.system(cmd_crop.format(imgIname,CROP_HEIGHT,CROP_OFF_Y, imgCname))
    else:
        os.system(cmd_chop.format(imgIname, CHOP_HEIGHT,imgCname))
    return imgCname

cmd_combine = magick + " -adaptive-sharpen 0x{} -append {} \"{}\""
def combineCropedImgs(imgCnames):
    imgClongstr = ""
    for imgCname in imgCnames:
        imgClongstr += " \"{}\" ".format(imgCname)

    imgLname, imgLext = os.path.splitext(imgCnames[-1])
    imgLname = imgLname + "_long_{}".format(len(imgCnames)) + imgLext
    print("{} imgs combined.".format(len(imgCnames)))
    os.system(cmd_combine.format(SHARPEN,imgClongstr, imgLname))
    return imgLname

def short2long(imgInames):
    imgInames = sortImgs(imgInames)
    imgCnames = []

    for i in range(len(imgInames)):
        imgCname = cropImg(imgInames[i],i==0)
        imgCnames.append(imgCname)

    combineCropedImgs(imgCnames)

    for i in range(0, len(imgInames)):
        os.remove(imgCnames[i])

if __name__ == '__main__':
    pass