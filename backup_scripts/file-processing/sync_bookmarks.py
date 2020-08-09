import os
import time
t0 = time.time()

mark_str_body = "BookmarkBegin\nBookmarkTitle: {}\nBookmarkLevel: {}\nBookmarkPageNumber: {}\n"

# book_fname = "镜头的语法.pdf"
# txt_fname =  "bk-camera-i.txt"
# mark_fname = "bk-camera.txt"
book_fname = "破坏之王-DDoS攻击与防范深度剖析.pdf"
txt_fname =  "bk-phzw-i.txt"
mark_fname = "bk-phzw.txt"

page_offset = 13 # means page 1 in .txt is page (1+13=)14 in .pdf
def write_bookmark_from_txt():
    with open(txt_fname,encoding='utf-8', mode = 'r') as rf:
        lines = rf.readlines()

    mark_str = ""
    level = 1
    status = 0
    for line in lines:
        if len(line.strip()) == 0:
            continue
        if status == 0:
            title = line.strip()
            status = 1
            continue
        else:
            tmp_L = list(map(int,line.split()))
            page_num = tmp_L[0]
            level = level if len(tmp_L) == 1 else tmp_L[1]

            # print(title, page_num, level)
            mark_str+=mark_str_body.format(title.encode('ascii', 'xmlcharrefreplace').decode('utf-8'), level, max(1,page_num+page_offset))
            status = 0

    with open(mark_fname,"w") as wf:
        wf.write(mark_str)

# write_bookmark_from_txt()
name,ext = os.path.splitext(book_fname)
# os.system("pdftk \"{}\" dump_data output {}".format(book_fname,mark_fname))
os.system("pdftk \"{}\" update_info {} output \"{}\"".format(book_fname, mark_fname, name+"【书签】"+ext))

print("Elapsed time: {}s".format(round(time.time()-t0,1)))