import yt_dlp

url = 'https://www.youtube.com/watch?v=jyHQK1yUJqQ'

ydl_opts = {
    'format': 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best',
    'outtmpl': '/usr/DATA/backup_home_dir/jhhan/02_dev/llm/stt/whisper/Whisper-WebUI/data/youtube/input2.mp4',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])