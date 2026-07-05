
### progress bar for ffmpeg
def ffmpeg_progress_hook(block_num, block_size, total_size):
    if total_size > 0:
        downloaded = block_num * block_size
        percent = min(int(downloaded * 100 / total_size), 100)
        filled = percent // 2
        bar = "█" * filled + "░" * (50 - filled)
        print(f"\rDownloading: |{bar}| {percent}%", end="", flush=True)
    else:
        print(f"\rDownloaded: {block_num * block_size / 1024:.0f} KB", end="", flush=True)

### progress bar for video download
def video_progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded = d.get('downloaded_bytes', 0)
        if total > 0:
            percent = min(int(downloaded * 100 / total), 100)
            filled = percent // 2
            bar = "█" * filled + "░" * (50 - filled)
            speed = d.get('speed', 0)
            speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "?"
            eta = d.get('eta', 0)
            eta_str = f"{eta}s" if eta else "?"
            print(f"\rDownloading: |{bar}| {percent}%  {speed_str}  ETA: {eta_str}", end="", flush=True)
    elif d['status'] == 'finished':
        print("\n[✓] Downloaded, now processing...")