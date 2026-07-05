import yt_dlp
from ffmpeg_setup import setup_ffmpeg
from progress_bar import video_progress_hook

class YTRunner:
    def __init__(self):
        self.quality_map = {
            "1": "bestvideo[height<=1080]+bestaudio/best",
            "2": "bestvideo[height<=720]+bestaudio/best",
            "3": "bestvideo[height<=480]+bestaudio/best",
            "4": "bestaudio/best",
        }
        self.ffmpeg_path = setup_ffmpeg()

    def execute_download(self, url, choice):
        selected_format = self.quality_map.get(choice)

        if not selected_format:
            print("⨯ Invalid quality selection")
            return False

        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "format": selected_format,
            "progress_hooks": [video_progress_hook],
            "extractor_args": {"youtube": {"skip": ["dash", "hls"]}},
            "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"},
        }
        
        if self.ffmpeg_path:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_path

        if choice == "4":
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        try:
            print(f"\n Downloader starting stream fetch for: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"⨯ Downloader Error: {e}")
            return False