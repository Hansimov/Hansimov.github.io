import os
import platform
import shutil

mode = 1 # 1: origin to hanslab, 2: hanslab to origin

pc_name = platform.node()

if pc_name == "DESKTOP-BQVCMQA":
    user_name = "yuzeh"
elif pc_name == "trevize":
    user_name = "20133"
else:
    user_name = "yzh"

custom_css_name = "custom.css"
notebook_json_name = "notebook.json"

custom_css_full_name = "C:/Users/{}/.jupyter/custom/".format(user_name) + custom_css_name
notebook_json_full_name = "C:/Users/{}/.jupyter/nbconfig/".format(user_name) + notebook_json_name

if mode == 1:
    src_custom_css_name, dst_custom_css_name = custom_css_full_name, custom_css_name
    src_notebook_json_name, dst_notebook_json_name = notebook_json_full_name, notebook_json_name
else:
    src_custom_css_name, dst_custom_css_name = custom_css_name, custom_css_full_name
    src_notebook_json_name, dst_notebook_json_name = notebook_json_name, notebook_json_full_name

shutil.copyfile(src_custom_css_name, dst_custom_css_name)
shutil.copyfile(src_notebook_json_name, dst_notebook_json_name)

