import re
import tkinter as tk
from tkinter import filedialog, font
from customtkinter import CTkEntry, CTkButton
from pytube import YouTube
import winsound

# Initialize the main window
root = tk.Tk()

root.title("YouTube Downloader")
root.geometry("889x500")
root.config(bg='#302E2E')
root.resizable(False, False)

# Define fonts
title_font = font.Font(family='Press Start 2P', size=20)
button_font = font.Font(family='Fira Code', size=14)

# Heading label
heading_label = tk.Label(text='YouTube Downloader', font=title_font, bg='#302E2E', fg='#FFFFFF')
heading_label.grid(row=0, column=3, padx=230, pady=30, sticky="w")

# Link entry field
link_field1 = CTkEntry(master=root,
                       font=('Fira Code', 15),
                       fg_color='#302E2E',
                       width=625,
                       text_color='white',
                       height=38,
                       border_width=1,
                       corner_radius=10,
                       placeholder_text="Paste the link")
link_field1.grid(row=3, column=3, padx=150, pady=20, sticky="w")

# File path entry field
file_field = CTkEntry(master=root,
                      font=('Fira Code', 15),
                      fg_color='#302E2E',
                      width=440,
                      text_color='white',
                      height=38,
                      border_width=1,
                      corner_radius=10,
                      placeholder_text="Select the Folder",
                      state='disabled')
file_field.grid(row=6, column=3, padx=150, pady=20, sticky="w")

# Label to display completion message
completion_label = tk.Label(master=root,
                            text='',
                            font=button_font,
                            bg='#302E2E',
                            fg='#FFFFFF')
completion_label.grid(row=9, column=3, padx=350, pady=20, sticky="w")


# Function to select the path
def select_path():
    file = filedialog.askdirectory(title="Select Folder")

    file_field.configure(state="normal")
    file_field.delete(0, tk.END)
    if file:
        file_field.insert(0, file)
    else:
        file_field.insert(0, "Select the folder")
    file_field.configure(state="disabled")


# Function to sanitize the filename
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def play_sound(sound_type):
    if sound_type == "complete":
        winsound.PlaySound("complete.wav", winsound.SND_FILENAME)
    elif sound_type == "error":
        winsound.PlaySound("error.wav", winsound.SND_FILENAME)


# Function to download audio
def audio_download():
    urls = link_field1.get()
    output_path = file_field.get()

    if not urls or output_path == "Select the folder":
        print("Please provide both the link and the folder path.")
        completion_label.config(text="Please provide link and folder path.", fg='#FF0000')
        completion_label.grid(row=9, column=3, padx=250, pady=20, sticky="w")
        play_sound("error")
        return

    vid = YouTube(urls)
    audio_stream = vid.streams.filter(only_audio=True).first()
    entry = sanitize_filename(vid.title)

    print(f"\nVideo found: {entry}\n")

    print("Downloading Audio...")
    audio_stream.download(output_path, filename=f"{entry}.mp3")
    print("Audio download completed.")
    completion_label.config(text="Download completed!", fg='#00FF00')
    completion_label.grid(row=9, column=3, padx=350, pady=20, sticky="w")
    play_sound("complete")

# Function to download video
def video_download():
    urls = link_field1.get()
    output_path = file_field.get()

    if not urls or output_path == "Select the folder":
        print("Please provide both the link and the folder path.")
        completion_label.config(text="Please provide link and folder path.", fg='#FF0000')
        completion_label.grid(row=9, column=3, padx=250, pady=20, sticky="w")
        play_sound("error")
        return

    vid = YouTube(urls)
    video_stream = vid.streams.filter(progressive=True, res="1080p").first()
    entry = sanitize_filename(vid.title)

    if not video_stream:
        print("1080p video not available as a single stream with audio.")
        video_stream = vid.streams.filter(progressive=True).order_by('resolution').desc().first()

    print(f"\nVideo found: {entry}\n")

    print("Downloading Video...")
    video_stream.download(output_path, filename=f"{entry}.mp4")
    print("Video download completed.")
    completion_label.config(text="Download completed!", fg='#00FF00')
    completion_label.grid(row=9, column=3, padx=350, pady=20, sticky="w")
    play_sound("complete")

# Browse button
browse_button = CTkButton(master=root,
                          font=('Fira Code', 15),
                          fg_color='#AF2D2D',
                          width=150,
                          text='Browse Folder',
                          text_color='white',
                          height=38,
                          anchor='right',
                          command=select_path,
                          hover_color='#DF7C7C')
browse_button.grid(row=6, column=3, padx=620, pady=20, sticky="e")

# Mp3 convert button
yt_audio = CTkButton(master=root,
                     font=('Fira Code', 15),
                     fg_color='#AF2D2D',
                     width=300,
                     text='Mp3 convert',
                     text_color='white',
                     height=38,
                     hover_color='#DF7C7C',
                     command=audio_download)
yt_audio.grid(row=8, column=3, padx=150, pady=20, sticky="w")

# Mp4 convert button
yt_video = CTkButton(master=root,
                     font=('Fira Code', 15),
                     fg_color='#AF2D2D',
                     width=300,
                     text='Mp4 convert',
                     text_color='white',
                     height=38,
                     hover_color="#DF7C7C",
                     command=video_download)
yt_video.grid(row=8, column=3, padx=475, pady=20, sticky="w")

# Run the main loop
root.mainloop()