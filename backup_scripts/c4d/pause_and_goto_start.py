import c4d

def main():
    if c4d.CheckIsRunning(c4d.CHECKISRUNNING_ANIMATIONRUNNING):
        c4d.CallCommand(12412) # Play Forwards
    c4d.CallCommand(12501) # Go to Start

if __name__=='__main__':
    main()