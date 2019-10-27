import os

home = "./"

def delelteOut(imgname):
    name,ext = os.path.splitext(imgname)
    if not ext in [".jpg",".png",".jpeg",".bmp",".gif",".webm",".mp4"]:
        pass
    else:
        if name.endswith(("_out","_resize","副本","_combined")):
            print("Deleting {} ...".format(imgname))
            os.remove(imgname)
    # else:
    #     print("* Ignore ",imgname)

if __name__ == '__main__':
    for imgname in os.listdir(home):
        delelteOut(imgname)
