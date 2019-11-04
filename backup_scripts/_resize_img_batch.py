import os
from PIL import Image, ImageFilter
# from _combine_img_batch import *

home = './'
magick = "D:/ImageMagick/magick.exe convert "
cmd_resize_img = magick + " \"{}\" -resize {}x{} \"{}\""

ratiow,ratioh = 800,1200
def resizeWH(w,h):
    if w<=h:
        wr,hr = ratiow, h/w*ratiow
    else:
        wr,hr = ratioh, h/w*ratioh
    return int(wr),int(hr)

def resizeImg(imgname):
    name,ext = os.path.splitext(imgname)
    img = Image.open(imgname)
    w,h = img.size
    wr,hr = resizeWH(w,h)
    # imgr = img.resize((wr,hr))
    imgrname = name+"_resize"+ext

    os.system(cmd_resize_img.format(imgname,wr,hr,imgrname))
    # imgr.save(imgrname)
    # os.remove(imgrname)

def resizeThis(imgname):
    name,ext = os.path.splitext(imgname)
    if ext in [".jpeg",".jpg",".png",".bmp"]:
        print("Resizing ", imgname)
        resizeImg(imgname)
    else:
        print("* Ignore ",imgname)


if __name__ == '__main__':
    # for imgname in os.listdir(home):
    #     resizeThis(imgname)
    # pass
    # appendImg("disharmonica-lying-2b.jpg")
    imgname = "z.jpeg"
    resizeThis(imgname)