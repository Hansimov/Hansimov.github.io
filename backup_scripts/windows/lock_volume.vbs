Set objShell = WScript.CreateObject("WScript.Shell")
Do While True
objShell.Run("nircmdc loop 172800 1000 setsysvolume 57016 default_record"), 0, True
Loop