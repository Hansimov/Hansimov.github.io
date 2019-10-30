import os
import requests
from multiprocessing.dummy import Pool

imgnum = 20

imglinktxt = "_imglink.txt"

# with open(imglinkstxt,"w") as wf:
#     for i in range(imgnum):
#         print(imgbody.format(i+1),file=wf)

imglinks = []
with open(imglinktxt,"r") as rf:
    imglink = rf.read().strip()
    urlhead, imgname = os.path.split(imglink)
    print(urlhead, imgname)
    imgpath,ext = os.path.splitext(imgname)
    # print(imgpath,ext)
    imgnum = int(imgpath[-2:])
    # print(imgnum)

    for i in range(imgnum):
        imglink = "{}/{}{:0>2}{}".format(urlhead,imgpath[:-2],i+1,ext)
        imglinks.append(imglink)
    print(imglinks)

# imglinks = []
# with open(imglinkstxt,mode="r") as imglinksfile:
#     for line in imglinksfile:
#         # print(line.strip())
#         imglinks.append(line.strip())
# # print(imglinks)

# # imgpath = os.path.split(os.path.splitext(imglinks[0])[0])[-1]
# imgpath = os.path.splitext(os.path.split(imglinks[-1])[-1])[0]
# # print(imgpath)
if not os.path.exists(imgpath):
    os.mkdir(imgpath)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'referer': 'https://www.metarthunter.com/'
}

def getImage(imglink):
    try:
        imgreq = requests.get(imglink,headers=headers)
        print('{} Getting image: {}'.format(imgreq, imglink))
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