import yt_dlp
import tkinter as tk
import sys
import os
from tkinter import ttk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def DLVideo():
    selectedUrl = entry.get()
    mp3check = asmp3.instate(["selected"])

    opts = {"ffmpeg_location": resource_path("ffmpeg\\ffmpeg.exe")}

    if mp3check is True:
        print(resource_path("ffmpeg\\ffmpeg.exe"))
        
        opts["format"] = 'mp3/bestaudio/best'
        opts["postprocessors"] = [{
            'key': "FFmpegExtractAudio",
            'preferredcodec': "mp3"
        }]


    if not selectedUrl:
        print("No URL!")
        return
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download(selectedUrl)

window = tk.Tk()
window.title("Merc's Simple Vid Downloader")
window.geometry("400x100")

hlo = ttk.Label(text="Video URL")
hlo.pack()

entry = tk.Entry(width=300)
entry.pack()

asmp3 = ttk.Checkbutton(text="Download MP3 only")
asmp3.state(["!alternate"])
asmp3.pack()

dlbutton = ttk.Button(text="Download", command=DLVideo)
dlbutton.pack()

window.mainloop()