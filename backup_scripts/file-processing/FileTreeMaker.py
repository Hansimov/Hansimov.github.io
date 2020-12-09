"""FileTreeMaker.py: ..."""

__author__   = "legendmohe"
__modified__ = "Hansimov"

root = "oai5g-v1.2.2/openair3/"
out_file = "openair3.txt"

ONLY_PRINT_NO_EMPTY_FOLDERS = True
ONLY_INCLUDED_EXTENSTION_L = [".c"]
ONLY_EXLUDED_EXTENSTION_L = []

import os
import argparse
import time

class FileTreeMaker(object):

    def _recurse(self, parent_path, file_list, prefix, output_buf, level):
        if len(file_list) == 0 \
            or (self.max_level != -1 and self.max_level <= level):
            return
        else:
            file_list.sort(key=lambda f: os.path.isfile(os.path.join(parent_path, f)))
            for idx, sub_path in enumerate(file_list):
                if any(exclude_name in sub_path for exclude_name in self.exn):
                    continue

                full_path = os.path.join(parent_path, sub_path)
                idc = "┣━ "
                if idx == len(file_list) - 1:
                    idc = "┗━ "

                if os.path.isdir(full_path) and sub_path not in self.exf:
                    output_buf.append("%s%s[%s]" % (prefix, idc, sub_path))
                    if len(file_list) > 1 and idx != len(file_list) - 1:
                        tmp_prefix = prefix + "┃  "
                    else:
                        tmp_prefix = prefix + "    "

                    len_output_buf_old = len(output_buf)
                    self._recurse(full_path, os.listdir(full_path), tmp_prefix, output_buf, level + 1)
                    len_output_buf_new = len(output_buf)
                    if ONLY_PRINT_NO_EMPTY_FOLDERS and len_output_buf_new <= len_output_buf_old:
                        output_buf.pop()

                elif os.path.isfile(full_path):
                    # Add excluded extension here
                    name, ext = os.path.splitext(full_path)
                    if ONLY_INCLUDED_EXTENSTION_L:
                        if ext in ONLY_INCLUDED_EXTENSTION_L:
                            output_buf.append("%s%s%s" % (prefix, idc, sub_path))
                    elif ONLY_EXLUDED_EXTENSTION_L:
                        if ext not in ONLY_EXLUDED_EXTENSTION_L:
                            output_buf.append("%s%s%s" % (prefix, idc, sub_path))
                    else:
                        output_buf.append("%s%s%s" % (prefix, idc, sub_path))


    def make(self, args):
        self.root = args.root
        self.exf = args.exclude_folder
        self.exn = args.exclude_name
        self.max_level = args.max_level

        # print("root:%s" % self.root)

        buf = []
        path_parts = self.root.rsplit(os.path.sep, 1)
        buf.append("[%s]" % (path_parts[-1],))
        self._recurse(self.root, os.listdir(self.root), "", buf, 0)

        output_str = "\n".join(buf)
        if len(args.output) != 0:
            with open(args.output, 'w') as of:
                of.write(output_str)
        return output_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--root", help="root of file tree", default=root)
    parser.add_argument("-o", "--output", help="output file name", default=out_file)
    parser.add_argument("-xf", "--exclude_folder", nargs='*', help="exclude folder", default=[])
    parser.add_argument("-xn", "--exclude_name", nargs='*', help="exclude name", default=[])
    parser.add_argument("-m", "--max_level", help="max level",
                        type=int, default=-1)
    args = parser.parse_args()
    print(FileTreeMaker().make(args))


# import os
# root = "oai5g-v1.2.2/openair3/"
# # print(os.walk(root))
# for root, dirs, files in os.walk(root):
#     # print(root,dirs,files)
#     path = root.split(os.sep)
#     print("{} {}".format((len(path) - 1) * "--", os.path.basename(root)).strip())
#     for file in files:
#         name,ext = os.path.splitext(file)
#         if ext in [".c"]:
#             print("{} {}".format(len(path) * "--", file))
