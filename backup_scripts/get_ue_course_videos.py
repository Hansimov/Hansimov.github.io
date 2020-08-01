"""
* FFmpeg Filters Documentation 
    * http://ffmpeg.org/ffmpeg-filters.html#subtitles
* HowToBurnSubtitlesIntoVideo – FFmpeg 
    * https://trac.ffmpeg.org/wiki/HowToBurnSubtitlesIntoVideo
* ffmpeg subtitles alignment and position - Stack Overflow 
    * https://stackoverflow.com/questions/57869367/ffmpeg-subtitles-alignment-and-position
* How to Add Font size in subtitles in ffmpeg video filter - Stack Overflow 
    * https://stackoverflow.com/questions/21363334/how-to-add-font-size-in-subtitles-in-ffmpeg-video-filter

* ASS File Format Specification 
    * http://www.tcax.org/docs/ass-specs.htm
* date - How can I parse a time string containing milliseconds in it with python? - Stack Overflow 
    * https://stackoverflow.com/questions/698223/how-can-i-parse-a-time-string-containing-milliseconds-in-it-with-python
* Python timedelta issue with negative values - Stack Overflow 
    * https://stackoverflow.com/questions/8408397/python-timedelta-issue-with-negative-values
"""

import os
import requests
import re
import datetime

url_m3u8 = ""
url_vtt = ""
idx = 0
fname = ""

with open("links.txt", encoding="utf-8",mode="r") as rf:
    lines = rf.readlines()

cmd_dl_m3u8 = "ffmpeg -y -i \"{}\" -c copy -bsf:a aac_adtstoasc \"{}.mp4\""
cmd_vtt2ass = "ffmpeg -y -i \"{}.vtt\" \"{}.ass\""
# cmd_ass_in_mp4 = "ffmpeg -y -i \"{}.mp4\" -vf \"ass={}.ass\" \"{}.mp4\""
cmd_ass_in_mp4 = "ffmpeg -y -i \"{}.mp4\" -vf \"subtitles={}.ass:force_style='Fontsize=25,MarginV=30'\" \"{}.mp4\""

def str2dt(t_str):
    return datetime.datetime.strptime(t_str, "%H:%M:%S.%f")

MIN_OFFSET = 0.05
def correct_ass_timeline(ass_fname):
    with open(ass_fname+".ass", encoding="utf-8", mode="r") as rf:
        dials = rf.readlines()

    old_dial_start_dt, old_dial_end_dt = -1, -1

    out_str = ""
    for dial in dials:
        # dial = dial.strip()
        if not dial.startswith("Dialogue"):
            out_str += dial
            continue
        new_dial_start_str, new_dial_end_str = re.findall(r"\d+:\d+:\d+\.\d+", dial)
        # print(dial_begin, dial_end)
        # print(dial)
        new_dial_start_dt, new_dial_end_dt = str2dt(new_dial_start_str), str2dt(new_dial_end_str)
        # print(dial_begin_dt, dial_end_dt)
        print(new_dial_start_str, new_dial_end_str)
        if old_dial_start_dt == -1 or old_dial_end_dt == -1:
            out_str += dial
            pass
        else:
            # print(dial)
            delta_sec = (new_dial_start_dt-old_dial_end_dt).total_seconds()
            print(delta_sec)
            if delta_sec < 0:
                if abs(delta_sec) <= MIN_OFFSET:
                    corrected_dial = dial.replace(new_dial_start_str, old_dial_end_str)
                    out_str += corrected_dial
                else:
                    out_str += dial
            else:
                out_str += dial


        old_dial_start_dt, old_dial_end_dt = new_dial_start_dt, new_dial_end_dt
        old_dial_start_str, old_dial_end_str = new_dial_start_str, new_dial_end_str

    with open(ass_fname+"_new.ass", encoding="utf-8", mode="w") as wf:
        wf.write(out_str)


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
        ass_fname = "{:0>2}_tmp".format(idx)
        ass_fname_new = "{:0>2}_tmp_new".format(idx)
        status = 0
        # r = requests.get(url_vtt)
        # with open("{}.vtt".format(fname), "wb") as wf:
        #     wf.write(r.content)
        # os.system(cmd_dl_m3u8.format(url_m3u8, fname_tmp))
        # os.system(cmd_vtt2ass.format(fname, ass_fname))
        correct_ass_timeline(ass_fname)
        os.system(cmd_ass_in_mp4.format(fname_tmp, ass_fname_new, fname))

