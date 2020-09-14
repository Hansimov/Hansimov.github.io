import os

in_fname = "黑客攻防技术宝典 - Web实战篇 第2版.pdf"
out_fname = "黑客攻防技术宝典 - Web实战篇 第2版_.pdf"

cmd_rm_wm = "gswin64c -o \"{}\" -sDEVICE=pdfwrite -dFILTERTEXT \"{}\""
os.system(cmd_rm_wm.format(out_fname, in_fname))