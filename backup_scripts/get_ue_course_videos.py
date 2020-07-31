import os
import requests

url_m3u8 = ""
url_vtt = ""
idx = 0
fname = ""

with open("links.txt", encoding="utf-8",mode="r") as rf:
    lines = rf.readlines()

cmd_dl_m3u8 = "ffmpeg -y -i \"{}\" -c copy -bsf:a aac_adtstoasc \"{}\".mp4"
cmd_vtt2ass = "ffmpeg -y -i \"{}\".vtt \"{}\".ass"
cmd_ass_in_mp4 = "ffmpeg -y -i \"{}\".mp4 -vf ass=\"{}\".ass \"{}\".mp4"

status = 0
for line in lines:
    line = line.strip()
    if len(line)==0 or line.startswith("#"):
        continue
    if status == 0:
        url_m3u8 = line
        status += 1
    elif status == 1:
        url_vtt = line
        status += 1
    else:
        str_L = line.split(" ", 1)
        idx = str_L[0]
        fname = "{:0>2}_{}".format(idx, str_L[1])
        fname_tmp = fname + "_tmp"
        status = 0
        r = requests.get(url_vtt)
        with open("{}.vtt".format(fname), "wb") as wf:
            wf.write(r.content)
        os.system(cmd_dl_m3u8.format(url_m3u8, fname_tmp))
        os.system(cmd_vtt2ass.format(fname, fname))
        os.system(cmd_ass_in_mp4.format(fname_tmp, fname, fname))
