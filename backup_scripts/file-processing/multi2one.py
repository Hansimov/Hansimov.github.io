import os

fn_L = os.listdir()
fn_L = [x for x in fn_L 
        if os.path.splitext(x)[1] == ".png"]
fn_L = sorted(fn_L)

cmd_mul2one = "magick convert -append {} {}"

def print_run(s):
    print(s, flush=True)
    os.system(s)

in_img = ""
out_img = ""
cnt = 0
out_num = 0
for i in range(len(fn_L)):
    fn = fn_L[i]
    cnt += 1
    in_img += " \"{}\" ".format(fn)
    if cnt==4 or i==len(fn_L)-1:
        out_num += 1
        out_img = " \"out_{:0>2}.png\" ".format(out_num)
        print_run(cmd_mul2one.format(in_img, out_img))
        cnt = 0
        in_img = ""
        out_img = ""