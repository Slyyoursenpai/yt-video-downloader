# YouTube Video Downloader

A simple YouTube downloader — paste a link, choose quality, and download. No manual FFmpeg installation needed.

## Features

- 1080p, 720p, 480p video, or MP3 audio
- Auto-downloads FFmpeg on first run (no manual setup)
- Auto-installs yt-dlp if missing
- Live progress bars with speed and ETA

main.py	- Entry point

downloader.py -	Download logic

ffmpeg_setup.py	- Auto-downloads FFmpeg

progress_bar.py	- Progress bars

**Requirements**
Python 3.7+
Internet connection (first run downloads ~100 MB FFmpeg binaries)

## Usage

```bash
pip install yt_dlp
python main.py

or just

python main.py

Then paste a YouTube link and choose your format.


