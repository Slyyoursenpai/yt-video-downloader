import yt_dlp

class YTRunner:
    def __init__(self):
        self.quality_map = {
            "1": "bestvideo[height<=1080]+bestaudio/best",
            "2": "bestvideo[height<=720]+bestaudio/best",
            "3": "bestvideo[height<=480]+bestaudio/best",
            "4": "bestaudio/best"
        }
        
    def execute_download(self, url, choice):
        selected_format = self.quality_map.get(choice)
        
        if not selected_format:
            print("⨯ Invalid quality selection")
            return False
        
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': selected_format 
        }
        
        if choice == "4":
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        
        try:
            print(f"\n Downloader starting stream fetch for: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"⨯ Downloader Error: {e}")
            return False