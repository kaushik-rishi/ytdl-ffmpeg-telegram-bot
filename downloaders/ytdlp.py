from yt_dlp import YoutubeDL
import os

def download_audio(video_url: str, uuid: str) -> bool:
    filename_without_ext = f'bucket/{uuid}'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename_without_ext,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        print(e)
    
    # to confirm if the file is downloaded or not
    full_filename = f"{filename_without_ext}.mp3"
    return os.path.isfile(full_filename), full_filename


if __name__ == "__main__":
    if download_audio(video_url="https://www.youtube.com/watch?v=J515oMBCuX4", uuid="sobit"):
        print("audio file downloaded!")
    else:
        print("issue downloading the audio file!")