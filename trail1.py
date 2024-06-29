from pytube import YouTube

def audio_download():
    urls = input("Enter the YouTube URL: ")

    vid = YouTube(urls)

    video_download = vid.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    audio_download = vid.streams.filter(only_audio=True).first()

    entry = vid.title

    print(f"\nVideo found: {entry}\n")

    print("Downloading Video...")
    video_download.download(filename=f"{entry}.mp4")
    print("Video download completed.")

    print("Downloading Audio...")
    audio_download.download(filename=f"{entry}.mp3")
    print("Audio download completed.")

    print("Program Completed")
