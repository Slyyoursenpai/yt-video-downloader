import sys
import subprocess

try:
    import yt_dlp
except ImportError:
    print("[~] yt-dlp not found, installing...")
    subprocess.check_call([sys.executable,"-m","pip","install","yt-dlp"])
    import yt_dlp
    
from downloader import YTRunner
    
def main():
    print("===== Youtube Downloader====")
    
    url = input("Paste your Youtube Link here: ").strip()
    if not url:
        print("Error: Link was not found.")
        return
    
    print("\n Choose download format:")
    print("1) 1080p Video\n2) 720p Video\n3) 480p Video\n4) MP3 Audio Only")
    choice = input("Enter value (1-4): ").strip()
    
    success = YTRunner().execute_download(url,choice)
    
    if success: 
        print("\n Success, Check downloaded file")
    else:
        print("\n Download failed")
        
if __name__ == "__main__":
    main()