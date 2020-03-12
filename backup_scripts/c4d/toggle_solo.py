import c4d

def main():
    if c4d.IsCommandChecked(431000059) :
        c4d.CallCommand(431000058)  # Viewport Solo Off
    else :
        c4d.CallCommand(431000059)  # switch it on

if __name__=='__main__':
    main()