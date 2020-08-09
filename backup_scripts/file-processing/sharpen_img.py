import os
from multiprocessing import Pool

# root = "./algo-intro/"
# outpath = "./algo-intro-out/"
# root = "./os/"
# outpath = "./os-out/"
root = "./破坏之王/"
outpath = "./破坏之王-out/"
# cmd_sharpen = "magick convert -level 48%,100% -contrast-stretch 4% -adaptive-sharpen 0x3 -contrast -contrast \"{}\" \"{}\""
# cmd_sharpen = "magick convert -level 48%,100% -adaptive-sharpen 0x3 -contrast -contrast \"{}\" \"{}\""
# cmd_sharpen = "magick convert -level 40%,100% -contrast-stretch 4% -adaptive-sharpen 0x3 -contrast -contrast \"{}\" \"{}\""
# cmd_sharpen = "magick convert -level 40%,100% -adaptive-sharpen 0x3 -contrast -contrast \"{}\" \"{}\""
cmd_sharpen = "magick convert -adaptive-sharpen 0x5 \"{}\" \"{}\""

if not os.path.exists(outpath):
    os.mkdir(outpath)

imgList = os.listdir(root)

def sharpenImg(img_name):
    print("Processing: " + img_name)
    name,ext = os.path.splitext(img_name)
    out_img_name = name + "_out" + ext
    os.system(cmd_sharpen.format(root+img_name,outpath+out_img_name))

if __name__ == '__main__':
    # pool = Pool(5)
    # pool.map_async(sharpenImg,imgList).get(1)
    startPage,endPage = 0,10
    for img in imgList[startPage:]:
        sharpenImg(img)
