import os
from PIL import Image
import matplotlib.pyplot as plt

home = "./"
# def analyzeWH()

exts = [".jpg",".jpeg",".bmp",".png",".gif"]
ws = []
hs = []
names = []
for imgname in os.listdir(home):
    name,ext = os.path.splitext(imgname)
    if name.startswith("zzzz-") or name.endswith(("_副本","_blur","_stripe","_resize","_border","_blank","_invert","_out")) or not ext in exts:
        # print("* Ignore {}".format(imgname))
        pass
    else:
        img = Image.open(imgname)
        w,h = img.size
        ws.append(w)
        hs.append(h)
        names.append(name)
# print(ws,hs,names)

fig, ax = plt.subplots()
ax.scatter(ws,hs)
ax.plot(list(range(4000)))
for i, name in enumerate(names):
    ax.annotate(name, (ws[i], hs[i]))
    print(ws[i],hs[i],name)

plt.show()


