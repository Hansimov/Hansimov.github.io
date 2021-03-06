import re

# file_r = open('dx02.csv',encoding='utf-8',mode='r')
# file_w = open('dx02_w.txt','w')
# file_r = open('dx03.csv',encoding='utf-8',mode='r')
# file_w = open('dx03_w.txt','w')
file_r = open('dx04.csv',encoding='utf-8',mode='r')
file_w = open('dx04_w.txt','w')

# start = 31
# start = 61
start = 91

mode = 1
# mode == 1 :
#   Haven't met the body, discard all lines until a star
#   Have passed the body, discard all lines after.
# mode == 2 :
#   Have met real text and replace star with para number
#   Other lines will be remained and printed

for line in file_r.readlines():
    if line.startswith('--'):
        continue
    if mode == 1:
        if line.startswith('*'):
            mode = 2
            print(start,file=file_w)
        else:
            pass
    elif mode == 2:
        if line.startswith('*'):
            start += 1
            print('\n',start,file=file_w,sep='')
        elif line.startswith('$$$'):
            mode = 1
        else:
            print(line,file=file_w,end='')
    else:
        pass

file_w.close()
file_r.close()

