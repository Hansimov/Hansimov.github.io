import re
import os

mark_fname = "win-pe.txt"
out_mark_fname = "win-pe-o.txt"
book_fname = "Windows PE权威指南.pdf"

with open(mark_fname, mode="r", encoding="utf-8") as rf:
    lines = rf.readlines()

offset = 2
with open(out_mark_fname, mode="w", encoding="utf-8") as wf:
    for line in lines:
        line = line.strip()
        if line.startswith("PageMediaNumber") or line.startswith("BookmarkPageNumber"):
            res = re.match(r"(PageMedia|BookmarkPage)(Number.*?)(\d+)", line.strip())
            tmp = str(max(1, int(res[3])-2))
            tmp = res[1]+res[2]+tmp
            wf.write(tmp)
        else:
            wf.write(line)
        wf.write("\n")

name,ext = os.path.splitext(book_fname)
os.system("pdftk \"{}\" update_info {} output \"{}\"".format(book_fname, out_mark_fname, name+"【书签】"+ext))