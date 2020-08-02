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
import time
import datetime

links_fname = "links_animation.txt"
folder = "动画入门/"

if not os.path.exists(folder):
    os.mkdir(folder)

def headers():
    return { "user-agent": "botnet - {}".format(random.random()) }


def str2dt(t_str):
    return datetime.datetime.strptime(t_str, "%H:%M:%S.%f")


def fetch_vtt(url_vtt, vtt_folder, video_idx):
    seg_idx = 1
    try_cnt = 0
    status_code = 200

    while status_code == 200 or try_cnt <= 2:
        vtt_fname = "{:0>2}_{:0>2}.vtt".format(video_idx,seg_idx)
        print("Fetching {}".format(vtt_fname))
        if try_cnt == 0:
            url_vtt = re.sub(r"seg-\d+\.vtt", "seg-{}.vtt".format(seg_idx), url_vtt)
        r = requests.get(url_vtt)
        status_code = r.status_code
        print(status_code)
        if status_code != 200:
            try_cnt += 1
            # time.sleep(0.5)
            continue

        with open(vtt_folder+vtt_fname, mode="wb") as wf:
            wf.write(r.content)
        seg_idx += 1
        try_cnt = 0

def combine_vtt(vtt_folder):
    dial_L = []
    for item in os.listdir(vtt_folder):
        # print(item)
        with open(vtt_folder+item, encoding="utf-8", mode="r") as rf:
            lines = rf.readlines()

        time_str = ""
        dial_str = ""
        for line in lines:
            # print(line)
            line = line.strip()
            if len(line) == 0 or line.startswith("WEBVTT"):
                continue

            if re.match(r"\d+:\d+:\d+\.\d+", line):
                if len(dial_L) != 0 and time_str==dial_L[-1][0] and dial_str==dial_L[-1][1]:
                    continue
                else:
                    if time_str != "":
                        dial_L.append([time_str,dial_str.replace("\n"," ")])
                dial_str = ""
                time_str = line
            else:
                dial_str += line+"\n"

    vtt_str = "WEBVTT\n\n"
    for dial in dial_L:
        vtt_str += "{}\n{}\n".format(dial[0],dial[1])
    # print(vtt_str)
    vtt_fname = vtt_folder.strip("/")+".vtt"
    with open(vtt_fname, encoding="utf-8", mode="w") as wf:
        wf.write(vtt_str)
    return vtt_fname

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

    out_str = out_str.replace("\\N","\n")
    with open(ass_fname+".ass", encoding="utf-8", mode="w") as wf:
        wf.write(out_str)

cmd_vtt2ass = "ffmpeg -y -i \"{}.vtt\" \"{}.ass\""
def vtt2ass(vtt_fname):
    name, ext = os.path.splitext(vtt_fname)
    os.system(cmd_vtt2ass.format(name, name))
    correct_ass_timeline(name)

cmd_dl_m3u8 = "ffmpeg -y -i \"{}\" -c copy -bsf:a aac_adtstoasc \"{}.mp4\""
cmd_ass_in_mp4 = "ffmpeg -y -i \"{}.mp4\" -vf \"subtitles={}.ass:force_style='Fontsize=25,MarginV=30'\" \"{}.mp4\""

def download_m3u8_and_vtt():
    url_m3u8 = ""
    url_vtt = ""
    fname = ""

    url_L = []
    with open(links_fname, encoding="utf-8",mode="r") as rf:
        lines = rf.readlines()

    links_status = 0
    for line in lines:
        line = line.strip()
        if len(line)==0 or line.startswith("#"):
            continue
        if links_status == 0:
            str_L = line.split(" ", 1)
            video_idx = str_L[0]
            vtt_folder = folder+"{:0>2}/".format(video_idx) 
            if not os.path.exists(vtt_folder): 
                os.makedirs(vtt_folder)
            fname = "{:0>2} {}".format(video_idx, str_L[1])
            links_status += 1
        elif links_status == 1:
            url_m3u8 = line
            fname_tmp = fname + "_tmp"
            # os.system(cmd_dl_m3u8.format(url_m3u8, folder+fname_tmp))
            links_status += 1
        else:
            # fetch_vtt(line, vtt_folder, video_idx)
            vtt_fname = combine_vtt(vtt_folder)
            vtt2ass(vtt_fname)
            links_status = 0

            # ass_fname = "{:0>2}_tmp".format(idx)
            # ass_fname_new = "{:0>2}_tmp_new".format(idx)
            # status = 0
            # r = requests.get(url_vtt)
            # with open("{}.vtt".format(fname), "wb") as wf:
            #     wf.write(r.content)
            # os.system(cmd_vtt2ass.format(fname, ass_fname))
            # correct_ass_timeline(ass_fname)
            # os.system(cmd_ass_in_mp4.format(fname_tmp, ass_fname_new, fname))

download_m3u8_and_vtt()