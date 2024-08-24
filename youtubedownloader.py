import yt_dlp
import tkinter as tk
import sys
import os
import threading
from tkinter import ttk

downloading = False

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
        
        opts["progress_hooks"] = [SetProgressBar]
        opts["format"] = 'mp3/bestaudio/best'
        opts["postprocessors"] = [{
            'key': "FFmpegExtractAudio",
            'preferredcodec': "mp3"
        }]


    if not selectedUrl:
        print("No URL!")
        return
    
    global downloading
    if downloading:
        print("Already downloading!")
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        downloading = True
        dlbutton.config(text="Downloading...")
        pbar.pack()
        pbar.update()
        dlbutton.update()
        ydl.download(selectedUrl)
        dlbutton.config(text="Download")
        downloading = False
        pbar.pack_forget()

def StartDLVidThread():
    thread = threading.Thread(target=DLVideo)
    thread.start()

def SetProgressBar(prog):
    if prog["status"] == "downloading":
        print(prog)
        newstep = round( round( ( float(prog["downloaded_bytes"]) / float(prog["total_bytes"]) ) * 100 , 1 ) )
        print(newstep)
        pbarvar.set(newstep)
        pbar.update()
    elif prog["status"] == "finished":
        pbarvar.set(0)

def DoPopup(event):
    try:
        rmenu.tk_popup(event.x_root, event.y_root)
    finally:
        rmenu.grab_release()

def ClearEntry():
    entry.delete(0, tk.END)

def PasteEntry():
    entry.delete(0, tk.END)
    entry.insert(0, window.clipboard_get())

window = tk.Tk()
window.title("Merc's Simple Vid Downloader")
window.geometry("400x200")
window.configure(bg="#242322")

Style = ttk.Style()
Style.configure('custom.TCheckbutton', background="gray", font=('Bahnschrift'))
Style.configure('custom.TButton', background="green", font=('Bahnschrift'))

hlo = ttk.Label(text="Paste video URL below", font="Bahnschrift", background="gray")
hlo.pack(pady=10)
hlo.configure(borderwidth=8)

entry = tk.Entry(width=50)
entry.pack()
entry.configure(bg="gray")
entry.bind("<Button-3>", DoPopup)

rmenu = tk.Menu(entry, tearoff=0)
rmenu.add_command(label="Paste", command=PasteEntry)
rmenu.add_separator()
rmenu.add_command(label="Clear", command=ClearEntry)

asmp3 = ttk.Checkbutton(text="Download MP3 only", style="custom.TCheckbutton")
asmp3.state(["!alternate"])
asmp3.pack(pady=10)

dlbutton = ttk.Button(text="Download", command=StartDLVidThread, style="custom.TButton")
dlbutton.pack(pady=10)

pbarvar = tk.IntVar()
pbar = ttk.Progressbar(variable=pbarvar)

window.mainloop()