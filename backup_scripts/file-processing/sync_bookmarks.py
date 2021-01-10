import os
import time
t0 = time.time()

mark_str_body = "BookmarkBegin\nBookmarkTitle: {}\nBookmarkLevel: {}\nBookmarkPageNumber: {}\n"

# new_book_fname = "镜头的语法.pdf"
# txt_fname =  "bk-camera-i.txt"
# mark_fname = "bk-camera.txt"
# page_offset = 11

# new_book_fname = "剪辑的语法.pdf"
# txt_fname =  "bk-cut-i.txt"
# mark_fname = "bk-cut.txt"
# page_offset = 12

# old_book_fname = "组合 1.pdf"
# new_book_fname = "算法 原书第4版【高清】.pdf"
# txt_fname =  "bk-algo4-i.txt"
# mark_fname = "bk-algo4.txt"
# page_offset = 13

# old_book_fname = "C Primer Plus 第6版 中文.pdf"
# mid_book_fname = "组合 1.pdf"
# new_book_fname = "组合 1【书签】.pdf"
# mark_fname = "c-primer-plus.txt"
# write_mode = 1 # Extract bookmarks to .txt from "old" file, use "mid" file contents, generate "new" file

# old_book_fname = "Unix 网络编程 卷1：套接字联网API（第3版）.pdf"
# mid_book_fname = "组合 1.pdf"
# new_book_fname = "组合 1【书签】.pdf"
# mark_fname = "bk-unix-net-v1.txt"
# write_mode = 1 # Extract bookmarks to .txt from "old" file, use "mid" file contents, generate 

# old_book_fname = "Linux 高性能服务器编程【OCR】.pdf"
# mid_book_fname = "Linux 高性能服务器编程【OCR】.pdf"
# new_book_fname = "组合 1【书签】.pdf"
# mark_fname = "bk-linux-server.txt"
# write_mode = 1 # Extract bookmarks to .txt from "old" file, use "mid" file contents, generate "new" file

old_book_fname = "数据库系统概念 原书第6版【高清】.pdf"
mid_book_fname = "数据库系统概念 原书第6版【高清】.pdf"
new_book_fname = "组合 1【书签】.pdf"
mark_fname = "bk-db-sys.txt"
write_mode = 1


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

name,ext = os.path.splitext(old_book_fname)

if write_mode == 0: # from input .txt generate bookmarks, and write to "new" file
    write_bookmark_from_txt()
    # os.system("pdftk \"{}\" dump_data output {}".format(mid_book_fname,mark_fname))
    os.system("pdftk \"{}\" update_info {} output \"{}\"".format(old_book_fname, mark_fname, new_book_fname))
else: # write_mode == 1: Extract bookmarks to .txt from "old" file, use "mid" file contents, generate "new" file
    # os.system("pdftk \"{}\" dump_data output {}".format(old_book_fname, mark_fname))
    os.system("pdftk \"{}\" update_info {} output \"{}\"".format(mid_book_fname, mark_fname, new_book_fname))


print("Elapsed time: {}s".format(round(time.time()-t0,1)))