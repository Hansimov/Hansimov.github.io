import os
folder = "动画入门/"

mp4_L = [
    "01 动画 - 简介与原理",
    "02 动画 - 图解",
    "03 动画 - 建议",
]

cmd_burn_ass_into_mp4 = "ffmpeg -y -i \"{}.mp4\" -vf \"subtitles={}.ass:force_style='Fontsize=22,MarginV=30'\" \"{}.mp4\""

def merge_ass_into_mp4():
    for fname in mp4_L:
        name, ext = os.path.splitext(fname)
        os.system(cmd_burn_ass_into_mp4.format(folder+fname+"_tmp",folder+fname[0:2],folder+fname))

merge_ass_into_mp4()