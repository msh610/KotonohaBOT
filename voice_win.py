import win32com.client

def talkWin32(text, filename):
    sapi = win32com.client.Dispatch("SAPI.SpVoice")
    cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
    cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
    v = [t for t in cat.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Sayaka"]
    if v:
        fs = win32com.client.Dispatch("SAPI.SpFileStream")
        fs.Open(filename, 3)
        sapi.AudioOutputStream = fs
        oldv = sapi.Voice
        sapi.Voice = v[0]
        sapi.Speak(text)
        sapi.Voice = oldv
        fs.Close()