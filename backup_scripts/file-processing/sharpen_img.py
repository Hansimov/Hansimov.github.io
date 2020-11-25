import os
import time
# from multiprocessing import Pool

# root = "./algo-intro/"
# outpath = "./algo-intro-out/"

# root = "./os/"
# outpath = "./os-out/"
# cmd_sharpen = "magick convert -contrast -contrast -adaptive-sharpen 0x3 \"{}\" \"{}\""

# root = "./net/"
# outpath = "./net-out/"
# cmd_sharpen = "magick convert -contrast -contrast -contrast -adaptive-sharpen 0x3 \"{}\" \"{}\""
# # cmd_sharpen = "magick convert -contrast -contrast -contrast \"{}\" \"{}\""

# root = "./db/"
# outpath = "./db-out/"
# cmd_sharpen = "magick convert -adaptive-sharpen 0x4 \"{}\" \"{}\""
# cmd_sharpen = "magick convert -contrast -contrast -contrast \"{}\" \"{}\""

# root = "./win-prog/"
# outpath = "./win-prog-out/"
# cmd_sharpen = "magick convert -set option:deskew:auto-crop true -deskew 40% -resize 990x -adaptive-sharpen 0x3 \"{}\" \"{}\""
# cmd_sharpen = "magick convert -set option:deskew:auto-crop true -deskew 40% -adaptive-sharpen 0x4 \"{}\" \"{}\""

# root = "./Windows核心编程/"
# outpath = "./Windows核心编程-out/"
# cmd_sharpen = "magick convert -set option:deskew:auto-crop false -deskew 40% -resize 990x \"{}\" \"{}\""
# cmd_sharpen = "magick convert -set option:deskew:auto-crop true -deskew 40% -adaptive-sharpen 0x4 \"{}\" \"{}\""

# root = "./深入解析Windows操作系统 第6版 下册/"
# outpath = "./深入解析Windows操作系统 第6版 下册-out/"
# cmd_sharpen = "magick convert -level 60%,100% -contrast \"{}\" \"{}\""

# root = "./汇编语言x86/"
# outpath = "./汇编语言x86-out/"
# cmd_sharpen = "magick convert -level 70%,100% -contrast \"{}\" \"{}\""

# root = "./unix-networking-vol1/"
# outpath = "./unix-networking-vol1-out/"
# cmd_sharpen = "magick convert -set option:deskew:auto-crop false -deskew 10% -adaptive-sharpen 0x3 -resize 983x \"{}\" \"{}\""

root = "./linux-server/"
outpath = "./linux-server-out/"
cmd_sharpen = "magick convert -adaptive-sharpen 0x1 -set option:deskew:auto-crop false -deskew 80% -adaptive-resize 982x \"{}\" \"{}\"" # 60% is better than 40%
# cmd_sharpen = "magick convert -set option:deskew:auto-crop false -deskew 80% \"{}\" \"{}\""
# cmd_sharpen = "magick convert -set option:deskew:auto-crop false -deskew 80% -resize 1000x \"{}\" \"{}\""


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

    t1 = time.time()
    # start_page, end_page = -1,
    for img in imgList[:]:
        sharpenImg(img)
    t2 = time.time()

    print("Elapsed time: {}s".format(round(t2-t1),1))
