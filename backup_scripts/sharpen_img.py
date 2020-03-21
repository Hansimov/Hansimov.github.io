import os
from multiprocessing import Pool

root = "./game-engine/"
outpath = "./game-engine-out/"
cmd_sharpen = "magick convert -adaptive-sharpen 0x5 \"{}\" \"{}\""

if not os.path.exists(outpath):
    os.mkdir(outpath)

imgList = os.listdir(root)

def sharpenImg(infilename):
    print("Processing: " + infilename)
    name,ext = os.path.splitext(infilename)
    outfilename = name + "_out" + ext
    os.system(cmd_sharpen.format(root+infilename,outpath+outfilename))

if __name__ == '__main__':
    # pool = Pool(5)
    # pool.map_async(sharpenImg,imgList).get(1)
    startNum = 500
    for img in imgList[startNum-1:]:
        sharpenImg(img)
