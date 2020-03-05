import c4d

def main():
    c4d.CallCommand(12501) # Go to Start
    if not c4d.CheckIsRunning(c4d.CHECKISRUNNING_ANIMATIONRUNNING):
        c4d.CallCommand(12412) # Play Forwards
    

if __name__=='__main__':
    main()