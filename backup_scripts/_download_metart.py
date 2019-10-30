import os
import requests
from multiprocessing.dummy import Pool

imgnum = 20

imglinktxt = "_imglink.txt"

imglinks = []
with open(imglinktxt,"r") as rf:
    imglink = rf.read().strip()
    urlhead, imgname = os.path.split(imglink)
    imgpath,ext = os.path.splitext(imgname)
    imgnum = int(imgpath[-2:])

    for i in range(imgnum):
        imglink = "{}/{}{:0>2}{}".format(urlhead,imgpath[:-2],i+1,ext)
        imglinks.append(imglink)

if not os.path.exists(imgpath):
    os.mkdir(imgpath)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'referer': 'https://www.metarthunter.com/'
}

def getImage(imglink):
    try:
        imgreq = requests.get(imglink,headers=headers)
        print('{} Getting image: {}'.format(imgreq, imglink[-6:-4]))
        # print(imgreq)
    except Exception as e:
        print(e)
    else:
        name,ext = os.path.splitext(imglink)
        imgname = os.path.split(name)[-1] + ext

        with open(imgpath+"/"+imgname,'wb') as imgfile:
            imgfile.write(imgreq.content)

if __name__ == '__main__':
    pass
    # for imglink in imglinks:
    #     getImage(imglink)
    poolsize = len(imglinks)
    poolsize = 8
    pool = Pool(poolsize)
    pool.map_async(getImage, imglinks).get(200)