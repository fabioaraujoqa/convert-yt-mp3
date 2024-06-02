from pytube import YouTube
from pydub import AudioSegment
import os
from tqdm import tqdm

# Callback function to update progress bar
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    pbar.n = bytes_downloaded
    pbar.refresh()

def download_video(url, output_path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        video = yt.streams.filter(only_audio=True).first()
        global pbar
        pbar = tqdm(total=video.filesize, unit='B', unit_scale=True, desc='Downloading')
        downloaded_file = video.download(output_path=output_path)
        pbar.close()
        print(f"Downloaded: {downloaded_file}")
        return downloaded_file
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_to_mp3(file_path):
    try:
        audio_file_path = file_path.replace(".mp4", ".mp3")
        audio = AudioSegment.from_file(file_path)
        audio.export(audio_file_path, format="mp3")
        os.remove(file_path)
        print(f"Converted to MP3: {audio_file_path}")
        return audio_file_path
    except Exception as e:
        print(f"Error: {e}")
        return None

def download_and_convert(url, output_path):
    video_path = download_video(url, output_path)
    if video_path:
        convert_to_mp3(video_path)

if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    output_path = os.path.expanduser("~/Downloads")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    download_and_convert(url, output_path)
