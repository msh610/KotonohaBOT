import comtypes.client

def talkComtypes(text, filename):
    speak = comtypes.client.CreateObject("SAPI.SpVoice")
    filestream = comtypes.client.CreateObject("SAPI.spFileStream")
    filestream.open(filename, 3, False)
    speak.AudioOutputStream = filestream
    speak.Speak(text)
    filestream.close()
