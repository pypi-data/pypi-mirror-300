from yt_dlp import YoutubeDL


def extract_audio(url: str, output_path: str):
    ydl_opts = {"format": "bestaudio/best", "outtmpl": output_path}

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
