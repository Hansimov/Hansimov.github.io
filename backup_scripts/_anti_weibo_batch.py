# 一些尝试用于对抗色情图片检测算法的思路
#   https://github.com/wangx404/anti-NSFW-detection-test

import os
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import imageio
import subprocess
import cv2
import time
from colorthief import ColorThief

home = './'

magick = "D:/ImageMagick/magick.exe convert "
ffmpeg = "D:/ffmpeg/bin/ffmpeg.exe "

antimode = [2,3]                    # 1: tolong - 2: togif || 1: stripe - 2: blur  - 3: pure color
isPreviewPDF = False                # txt2pdf2png2gif: True: only output pdf || False: toGif
MASK_NUM = 2                        # imgToLong: num of masks
BLUR_RADIUS = 32                    # blurImg: GaussianBlur radius
STRIPE_STEP = 10                     # stripeImg: number of step of stripes
STRIPE_COLOR = 255                  # stripeImg: number of step of stripes
isResizeImg = True                  # imgToLong: is resize img before later processing
ratiow, ratioh = 800, 1000          # resizeImg: min image width (high or wide)
MAX_H = 8000                        # resizeImg: max image height
gsw = 600                           # resizeGif: gif max width
bg = (209,160,25)                 # genBG: background color
# bg = (0,0,0)                        # genBG: background color
gaph = 10                           # imgToLong: height gap between images
bgrw,bgrh = 1,4                     # genBG: ratio of width and height to original img
bdr = ((0,0),                       # borderImg: border of tolong (in ratio %): w>h
       (0,0))                       # borderImg: border of tolong (in ratio %): w<h
vrw = 400                           # video2gif: max gif width
vrt = 10 #                             # video2gif: max frame rate
VIDEO_DURATION_THRESHOLD = 5*1000  # video2gif: video duration threshold

tex_head = '''
\\documentclass[12pt]{article}
\\usepackage[UTF8]{ctex}
\\setCJKmainfont{Microsoft YaHei}
\\setmainfont{Microsoft YaHei} % 英文和数字也用雅黑
\\newfontfamily{\\tttnr}{Times New Roman}
\\newcommand*{\\tnr}{\\tttnr\\selectfont}
\\usepackage[active,tightpage]{preview}
\\renewcommand{\\PreviewBorder}{10pt}
\\newcommand{\\Newpage}{\\end{preview}\\begin{preview}}
\\usepackage{geometry}
\\geometry{
    paperwidth=350pt,
    top=2cm,
    left=2cm,
    right=2cm
}
\\usepackage{graphicx}
\\usepackage{xcolor}
\\usepackage{enumitem}
\\setlist{itemindent=1em,nolistsep,topsep=0pt,itemsep=0pt,partopsep=0pt,parsep=0pt}
\\obeylines
\\begin{document}
\\begin{preview}
'''

tex_tail = '''
\\end{preview}
\\end{document}
'''

def resizeWH(w,h):
    if w<=h:
        if h>=MAX_H:
            wr = min(ratiow, w/h*MAX_H)
            hr = h*wr/w
        else:
            wr,hr = ratiow, h/w*ratiow
    else:
        wr,hr = ratioh, h/w*ratioh
    return int(wr),int(hr)

cmd_resizeimg = magick + " \"{}\" -resize {}x{} \"{}\""
def resizeImg(img,name,ext):
    imgrname = name+"_resize"+ext
    w,h = img.size
    if isResizeImg:
        wr,hr = resizeWH(w,h)
    else:
        wr,hr = w,h
    # imgr = img.resize((wr,hr))
    # imgr.save(imgrname)
    os.system(cmd_resizeimg.format(name+ext,wr,hr,imgrname))
    imgr = Image.open(imgrname)
    return imgr, imgrname, wr, hr

# cmd_blur = magick + " \"{}\" -blur 0x{} \"{}\""
# def blurImg(imgrname,name,ext):
def blurImg(imgr,name,ext):
    # imgb = Image.new(mode="1",size=(wr,hr),color="white")
    # print("Creating blur ...")
    imgb = imgr.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
    imgbname = name+"_blur{:>02}".format(BLUR_RADIUS)+ext
    imgb.save(imgbname)
    return imgb, imgbname
    # os.system(cmd_blur.format(imgrname,BLUR_RADIUS,imgbname))
    # return "", imgbname

cmd_pure = magick + " -size {}x{} xc:white \"{}\""
def pureImg(imgr,name,ext):
    imguname = name+"_pure"+ext
    pure_color = (40,40,40)
    # color_thief = ColorThief(name+"_resize"+ext)
    # pure_color = color_thief.get_color(quality=1)
    imgu = Image.new("RGB", imgr.size, pure_color)
    imgu.save(imguname)
    return imgu, imguname

def stripeImg(imgr,name,ext):
    imgr = imgr.convert("RGB")
    pixr = np.array(imgr)
    # print(pixr)
    # avgpix = np.array(list(map(lambda i: 0 if int(pixr[:,:,i].mean())>127 else 255, list(range(pixr.shape[2])))))
    # print(avgpix)

    if pixr.shape[0] > pixr.shape[1]: # h > w
        for i in range(STRIPE_STEP):
            pixr[i::STRIPE_STEP+1,::,:] = STRIPE_COLOR
    else:
        for i in range(STRIPE_STEP+1):
            pixr[::,i::STRIPE_STEP+2,:] = STRIPE_COLOR

    imgpname = name+"_stripe"+ext
    imgp = Image.fromarray(pixr)
    imgp.save(imgpname)
    return imgp, imgpname


# bg = (255, 153, 204)
# bg = (0,0,0)
bgstr = ",".join([str(i) for i in bg])
cmd_border = magick + " \"{}\" -bordercolor rgb("+bgstr+") -border {}x{} \"{}\""
def borderImg(img,name,ext):
    imgdname = name+"_border"+ext
    w, h = img.size
    bdrw,bdrh = bdr[w<h]
    # rw,rh = (20,100)
    os.system(cmd_border.format(name+ext, str(bdrw)+"%", str(bdrh)+"%", imgdname))
    # os.remove(imgdname)
    # imgd = Image.open(imgdname)
    return "",imgdname

def invertImg(img,name,ext):
    imginame = name+"_invert"+ext
    imgi = img.convert('RGB')
    imgi = ImageOps.invert(imgi)
    imgi.save(imginame)
    return imgi, imginame

def blankImg(img,name,ext,rw=1,rh=1,color=(255,255,255)):
    imgkname = name+"_blank"+ext
    w,h = img.size
    # pix = np.array(img)
    # avgpix = tuple(map(lambda i: int(pix[100:200,100:200,i].mean()), list(range(pix.shape[2]))))
    # imgk = Image.new(mode="RGB",size=(w,int(h)),color=avgpix)
    imgk = Image.new(mode="RGB",size=(int(rw*w),int(rh*h)),color=color)

    # arr = np.random.rand(h,w,3) * 255
    # imgk = Image.fromarray(arr.astype('uint8'))

    imgk.save(imgkname)
    return imgk, imgkname

cmd_append = magick + " -append -background rgb("+ bgstr+") -gravity center {} \"{}\""

cmd_gif2img = magick + " \"{}\"[0] \"{}\""
def extractImg(gifname):
    name,ext = os.path.splitext(gifname)
    imgename = name+"_extract"+".jpg"
    os.system(cmd_gif2img.format(gifname,imgename))
    return "",imgename

def genBG(imgename):
    name,ext = os.path.splitext(imgename)
    imge = Image.open(imgename)
    # imgp,imgpname = stripeImg(imge, name, ".jpg")
    imgp,imgpname = blurImg(imge, name, ".jpg")
    imgb, imgbname = blankImg(imge,name,".jpg",bgrw,bgrh,bg)
    parts = [imgpname, imgbname, imgpname]

    imggname = name+"_bg"+".jpg"

    imgstr = " "
    for part in parts:
        imgstr += part + " "

    os.system(cmd_append.format(imgstr,imggname))
    os.remove(imgbname)
    os.remove(imgpname)

    return "",imggname

cmd_resizevideo = ffmpeg + " -y -i \"{}\" -vf \"scale='min({},iw)':-2\" -crf 28 \"{}\""
cmd_pale = ffmpeg + " -y -i \"{}\" -vf palettegen \"{}\""
# cmd_video2gif = ffmpeg + " -y -i {} -i {} -filter_complex paletteuse -r 10 {}"
# cmd_video2gif = ffmpeg + " -y -i {} -i {} -vf scale="+str(webmrw)+":-1 -r 10 {}"
cmd_video2gif = ffmpeg + " -y -i \"{}\" -i \"{}\" -filter_complex paletteuse -r {} \"{}\""
def video2gif(videoname):
    name,ext = os.path.splitext(videoname)
    palename = name + "_palette" + ".png"
    gifvname  = name + "_" +ext.replace(".","")+ ".gif"
    videorname = name + "_resize" + ext

    os.system(cmd_resizevideo.format(videoname,vrw,videorname))
    os.system(cmd_pale.format(videorname,palename))
    vrtx = min(vrt, int(cv2.VideoCapture(videorname).get(cv2.CAP_PROP_FPS)))
    os.system(cmd_video2gif.format(videorname,palename,vrtx,gifvname))
    os.remove(palename)
    os.remove(videorname)
    return gifvname

def resizeGif(gifname):
    name, ext = os.path.splitext(gifname)
    gifrname = name + "_resize" + ext
    gif = Image.open(gifname)
    w,h = gif.size
    gif.close()
    gswx = min(w,gsw)
    cmd_resizegif = magick + " \"{}\" -resize {}x \"{}\""
    os.system(cmd_resizegif.format(gifname,gswx,gifrname))
    return "",gifrname

def getFPS(img):
    img.seek(0)
    count,delay = 0,0
    while True:
        try:
            count += 1
            delay += img.info['duration']
            img.seek(img.tell()+1)
        except:
            FPS = count/delay * 1000
            print(count,FPS)
            break;

def getWH(imgname):
    name,ext = os.path.splitext(imgname)
    if not ext in [".jpg",".jpeg",".bmp",".png"]:
        return
    img = Image.open(imgname)
    w,h = img.size
    print("{:>4} {:>4} {:>5} {}".format(w,h,round(w/h,2),imgname))


cmd_append2 = magick + " -append -bordercolor SkyBlue -gravity South -border 0x100% {} {} {}"
# cmd_append3 = magick + " -append -bordercolor SkyBlue -border 0x30% {} {} {} {}"
cmd_append3 = magick + " -append -bordercolor SkyBlue -border 10%x30% {} {} {} {}"
# cmd_append3 = magick + " -append -background SkyBlue -splice 0%x30% -gravity south {} {} {} {}"
cmd_append3ratio = magick + " -append -bordercolor white -border {}%x{}% {} {} {} {}"

def imgToLong(imgname):
    print("Img to long: {}".format(imgname))
    name,ext = os.path.splitext(imgname)
    if ext in [".jpeg",".jpg",".png", ".bmp"]:
        pass
    else:
        return
    name,ext = os.path.splitext(imgname)

    parts = []

    img = Image.open(imgname)
    w,h = img.size
    imgr, imgrname,wr,hr = resizeImg(img,name,ext)
    if antimode[1] == 1:
        imgp, imgpname = stripeImg(imgr,name,ext)
    elif antimode[1] == 2:
        global BLUR_RADIUS
        # imgp, imgpname = blurImg(imgrname,name,ext)
        imgp, imgpname = blurImg(imgr,name,ext)
    for i in range(MASK_NUM):
        parts.append(imgpname)


    # imgk, imgkname = blankImg(img,name,ext)
    # imgi,imginame = invertImg(img,name,ext)
    rname,rext = os.path.splitext(imgrname)

    imgd, imgdname = borderImg(imgr,rname,rext)
    parts.append(imgdname)

    outname = name+"_out"+ext

    gaphstr = " \"xc:[x{}]\" ".format(gaph)
    imgstr = " "
    for part in parts:
        imgstr += "\"" + part + "\" " + gaphstr

    os.system(cmd_append.format(imgstr,outname))

    # os.remove(imgkname)
    # os.remove(imginame)
    os.remove(imgrname)
    os.remove(imgpname)
    os.remove(imgdname)

cmd_img2gif = magick + " -flatten {} -loop 1 \"{}\""
def img2gif(imgname):
    name,ext = os.path.splitext(imgname)
    img = Image.open(imgname)
    imgr, imgrname, wr, hr = resizeImg(img,name,ext)
    # imgb, imgbname = stripeImg(img,name,ext)
    if antimode[1] == 1:
        imgb, imgbname = stripeImg(imgr,name,ext)
    elif antimode[1] == 2:
        # imgb, imgbname = blurImg(imgrname,name,ext)
        imgb, imgbname = blurImg(imgr,name,ext)
    elif antimode[1] == 3:
        imgb, imgbname = pureImg(imgr,name,ext)
    # if wr < hr:
    #     imgb, imgbname = stripeImg(imgr,name,ext)
    # else:
    #     imgb, imgbname = blurImg(imgr,name,ext)

    outname = name+"_out"+".gif"
    print("Creating {} ...".format(outname))
    # os.system(cmd_imgs2gif.format(imgbname,imgname,outname))
    in_img_L = [imgbname, imgbname, imgrname, imgbname, imgbname]
    in_img_delay_L = [8, 8, 1500, 8, 8]
    in_img_str = ""
    for i in range(len(in_img_L)):
        in_img_str += " -delay {} \"{}\" ".format(in_img_delay_L[i], in_img_L[i])
    print(in_img_str)
    os.system(cmd_img2gif.format(in_img_str, outname))
    imgr.close()
    rm_tmp_imgs([imgrname, imgbname])

def rm_tmp_imgs(tmp_imgs):
    for img_name in tmp_imgs:
        os.remove(img_name)


# cmd_compgif = "convert {} null: ( {} -coalesce ) -gravity center -layers composite -fuzz 3% -layers OptimizeTransparency {}"
cmd_compgif = magick + "\"{}\" null: ( \"{}\" -coalesce ) -gravity center -layers composite -fuzz 5% -layers OptimizeTransparency \"{}\""
def gifToLong(gifname, isResize=True):
    print("Gif to long: {} ...".format(gifname))
    name,ext = os.path.splitext(gifname)
    outname = name+"_out"+ext

    if isResize==True:
        gifc, gifrname = resizeGif(gifname)
        imge, imgename = extractImg(gifrname)
        imgg, imggname = genBG(imgename)
        os.system(cmd_compgif.format(imggname,gifrname,outname))
        os.remove(gifrname)
    else:
        imge, imgename = extractImg(gifname)
        imgg, imggname = genBG(imgename)
        os.system(cmd_compgif.format(imggname,gifname,outname))

    os.remove(imgename)
    os.remove(imggname)

cmd_resizegif = magick + " \"{}\" -resize {}x{} \"{}\""
# cmd_gif2gif = magick  + " -delay 0 {} -loop 1 -delay 4 {} -duplicate 5,1--1 -fuzz 5% -layers OptimizeTransparency {}"
# cmd_gif2gif = magick  + " {} {} {}"
# cmd_gif2gif = magick  + " \"{}\" \"{}\" -fuzz 5% -layers OptimizeTransparency \"{}\""
cmd_gif2gif = magick  + " \"{}\" \"{}\" \"{}\""
def gif2gif(gifname,isResize=True):
    name,ext = os.path.splitext(gifname)
    imgename = name+"_extract.jpg"
    os.system(cmd_gif2img.format(gifname, imgename))
    imge = Image.open(imgename)

    outname = name+"_out"+".gif"
    if isResize==True:
        imgr, imgrname, wr, hr = resizeImg(imge, name,".jpg")
        print("Resizing {}".format(gifname))
        gifrname = name + "_resize" + ".gif"
        os.system(cmd_resizegif.format(gifname,wr,hr,gifrname))
        imgb, imgpname = blurImg(imgr, name, ".jpg")
        # imgb, imgpname = stripeImg(imgr, name, ".jpg")
        print("Creating {} ...".format(outname))
        os.system(cmd_gif2gif.format(imgpname, gifrname,outname))
        os.remove(imgrname)
        os.remove(gifrname)
    else:
        # imgb, imgpname = stripeImg(imge,name,".jpg")
        imgb, imgpname = blurImg(imge, name, ".jpg")
        print("Creating {} ...".format(outname))
        os.system(cmd_gif2gif.format(imgpname, gifname,outname))

    os.remove(imgename)
    os.remove(imgpname)

def antiVideo(videorname):
    name,ext = os.path.splitext(videorname)
    if   ext in [".webm",".mp4"]:
        gifvname = video2gif(videorname)
    else:
        gifvname = ""

    video =cv2.VideoCapture(videorname)
    video.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    if duration >= VIDEO_DURATION_THRESHOLD:
        gif2gif(gifvname,isResize=False)
    else:
        gifToLong(gifvname,isResize=False)

    os.remove(gifvname)

cmd_tex2pdf = "xelatex -aux-directory=latex-temp -interaction=batchmode {}"
cmd_pdf2png = 'gswin64c -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r288 -sOutputFile="{}" "{}"'
def txt2pdf2png2gif(filename):
    with open(filename, mode="r", encoding="utf-8") as rf:
        texts = rf.read()
        texts = texts.replace("\n\n","\\\\\n\n")
    texts = tex_head + texts + tex_tail
    name,ext = os.path.splitext(filename)
    texname = name + "_out.tex"
    with open(texname, mode="w", encoding="utf-8") as wf:
        print(texts,file=wf)
    pdfname = name+"_out.pdf"
    os.system(cmd_tex2pdf.format(texname))

    if not isPreviewPDF:
        pngname = name+"_out.png"
        os.system(cmd_pdf2png.format(pngname,pdfname))
        global ratiow
        ratiow = 400
        img2gif(pngname)
        os.remove(texname)
        # os.remove(pdfname)
        os.remove(pngname)

def antiWB(filename):
    global antimode
    name,ext = os.path.splitext(filename)
    if ext in [".jpg",".png",".jpeg",".bmp"]:
        if antimode[0] == 1:
            imgToLong(filename)
        else:
            img2gif(filename)
    elif ext == ".gif":
        gifToLong(filename)
    elif ext == ".txt":
        txt2pdf2png2gif(filename)
    elif ext in [".webm", ".mp4"]:
        antiVideo(filename)
    else:
        pass
if __name__ == '__main__':
    pass
    # videoname = "_txt2pdf.txt"
    # videoname = "z.png"
    # videoname = "z.mp4"
    videoname = "H:/图片/微博_归档/20200919-20201131-unused/studiofow-subverse-sidein-lily.jpeg"
    antiWB(videoname)