import os
from PIL import Image

magick = "D:/ImageMagick/magick convert "
ffmpeg = "D:/ffmpeg/bin/ffmpeg.exe "

cmd_append = magick + " -resize {} -append {} \"{}\""

resizew,resizeh = 800, 1200

def appendImg(imgnames):
    nameexts = []
    for imgname in imgnames:
        name,ext = os.path.splitext(imgname)
        nameexts.append([name,ext])
    nameexts = sorted(nameexts,key=lambda l:l[0], reverse=False)
    sortedimgnames = []
    for nameext in nameexts:
        sortedimgnames.append(nameext[0]+nameext[1])

    # print(sortedimgnames)

    imgstr = ""
    for imgname in sortedimgnames:
        imgstr += " \"{}\" ".format(imgname)

    # print(imgstr)
    print(sortedimgnames[-1])

    img = Image.open(imgname)
    w,h = img.size
    if w < h:
        resizestr = "{}x".format(resizew)
    else:
        resizestr = "{}x".format(resizeh)

    outname, ext = os.path.splitext(sortedimgnames[-1])
    outname = outname + "_combined" + ext
    os.system(cmd_append.format(resizestr, imgstr, outname))

if __name__ == '__main__':
    imgnames = [
        "sakimichan-birthday-gift-ahri-1.jpeg",
        "sakimichan-birthday-gift-ahri-2.jpeg",
        "sakimichan-birthday-gift-ahri-3.jpeg",
    ]

    appendImg(imgnames)