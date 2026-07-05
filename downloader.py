import os
import sys
import shutil
import urllib.request
import zipfile
import tarfile
import platform as _platform
import yt_dlp

# ── FFmpeg auto-setup ──────────────────────────────────────────────────

def _get_ffmpeg_info():
    system = sys.platform.lower()
    if system.startswith("win"):
        return {
            "url": "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip",
            "archive_type": "zip",
            "binary_name": "ffmpeg.exe",
            "probe_name": "ffprobe.exe",
            "inner_folder": "ffmpeg-master-latest-win64-gpl",
        }
    if system.startswith("linux"):
        return {
            "url": "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-linux64-gpl.tar.xz",
            "archive_type": "tar.xz",
            "binary_name": "ffmpeg",
            "probe_name": "ffprobe",
            "inner_folder": "ffmpeg-master-latest-linux64-gpl",
        }
    if system.startswith("darwin"):
        arch = _platform.machine()
        suffix = "arm64" if arch == "arm64" else "x86_64"
        return {
            "url": f"https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-darwin-{suffix}-gpl.zip",
            "archive_type": "zip",
            "binary_name": "ffmpeg",
            "probe_name": "ffprobe",
            "inner_folder": f"ffmpeg-master-latest-darwin-{suffix}-gpl",
        }
    return None


##def _progress_hook(block_num, block_size, total_size):
 ##   if total_size > 0:
  ##      downloaded = block_num * block_size
  ##      percent = min(int(downloaded * 100 / total_size), 100)
   ##     filled = percent // 2
   ##     bar = "█" * filled + "░" * (50 - filled)
   ##     print(f"\rDownloading: |{bar}| {percent}%", end="", flush=True)
   ## else:
   ##     print(f"\rDownloaded: {block_num * block_size / 1024:.0f} KB", end="", flush=True)


def setup_ffmpeg():
    """Locate or download FFmpeg. Returns the ffmpeg binary path, or None."""

    # 1. Already on PATH
    which = shutil.which("ffmpeg")
    if which:
        print(f"[✓] FFmpeg found: {which}")
        return which

    # 2. Already in local ffmpeg_bin/
    local_dir = "ffmpeg_bin"
    bin_name = "ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg"
    local_path = os.path.join(local_dir, bin_name)
    if os.path.isfile(local_path):
        print(f"[✓] FFmpeg found: {os.path.abspath(local_path)}")
        return os.path.abspath(local_path)

    # 3. Unsupported platform
    info = _get_ffmpeg_info()
    if info is None:
        print("[✗] Unsupported OS. Install FFmpeg manually: https://ffmpeg.org/download.html")
        return None

    # 4. Download
    print("[~] FFmpeg not found, downloading (~100 MB) ...")
    os.makedirs(local_dir, exist_ok=True)
    ext = ".zip" if info["archive_type"] == "zip" else ".tar.xz"
    archive_path = os.path.join(local_dir, "ffmpeg_dl" + ext)

    try:
        urllib.request.urlretrieve(info["url"], archive_path, _progress_hook)
        print()
    except Exception as e:
        print(f"\n[✗] Download failed: {e}")
        return None

    # 5. Extract
    tmp = os.path.join(local_dir, "_tmp")
    try:
        if info["archive_type"] == "zip":
            with zipfile.ZipFile(archive_path) as zf:
                zf.extractall(tmp)
        else:
            with tarfile.open(archive_path, "r:xz") as tf:
                tf.extractall(tmp)
    except Exception as e:
        print(f"[✗] Extraction failed: {e}")
        shutil.rmtree(tmp, ignore_errors=True)
        os.remove(archive_path)
        return None

    # 6. Copy binaries out of the nested folder into ffmpeg_bin/
    src_bin = os.path.join(tmp, info["inner_folder"], "bin")
    for name in (info["binary_name"], info["probe_name"]):
        src = os.path.join(src_bin, name)
        dst = os.path.join(local_dir, name)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

    shutil.rmtree(tmp, ignore_errors=True)
    os.remove(archive_path)

    final = os.path.abspath(os.path.join(local_dir, info["binary_name"]))
    print(f"[✓] FFmpeg ready: {final}")
    return final

# ── Downloader ─────────────────────────────────────────────────────────

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