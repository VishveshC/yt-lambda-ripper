import json
import os
from os import listdir
import sys
import urllib3
import telethon
from telethon import TelegramClient

def download_yt_dlp():
    url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
    target_path = "/tmp/yt-dlp"
    
    # Create a urllib3 PoolManager instance
    http = urllib3.PoolManager()

    try:
        # Perform GET request to fetch the file
        response = http.request('GET', url)

        # Raise exception for HTTP error codes
        if response.status != 200:
            raise Exception(f"Unexpected status code: {response.status}")
        
        # Write content to the file
        with open(target_path, "wb") as f:
            f.write(response.data)

        # Ensure it's executable
        os.chmod(target_path, 0o755)

        print("yt-dlp downloaded and made executable at:", target_path)
        return target_path
    except Exception as e:
        print("Error downloading yt-dlp:", e)
        return None


def lambda_handler(event, context):
    os.system('cp cookies.txt /tmp/cookies.txt')
    os.system('cp anoni.session /tmp/anoni.session')
    os.chdir('/tmp')
    download_yt_dlp()

    
    print(os.system('/tmp/yt-dlp -vU https://****** -o "%(title)s.%(ext)s" --concurrent-fragments 6 --restrict-filenames --no-check-certificates --progress-delta 5 --merge-output-format mkv --cache-dir /tmp/cache --cookies /tmp/cookies.txt --ffmpeg-location /opt/ffmpeg')) # Download video
    
    print("DOWNLOAD, MERGE COMPLETE")

    api_id = '******'
    api_hash = '******'
    phone_number = '+******'

    video = [f for f in os.listdir() if f.endswith((".mp4", ".mkv", ".webm"))] # Find video
    actualvideo = video[0] # Append video as a variable
    
    video_url = os.popen('/tmp/yt-dlp --skip-download https:****** --print webpage_url --no-warnings --cache-dir /tmp/cache --cookies /tmp/cookies.txt').read() # Download video url
    
    video_duration = int((os.popen('/tmp/yt-dlp --skip-download https://****** --print duration --no-warnings --cache-dir /tmp/cache --cookies /tmp/cookies.txt').read())) # Download video duration
    
    ss = video_duration - 3601 # seconds
    
    trim_cmd = f"/opt/ffmpeg -y -i /tmp/{actualvideo} -ss {ss} -to {video_duration} -c copy /tmp/trim_{actualvideo}"  # Trim 
    
    os.system(trim_cmd)
    os.system(f"rm /tmp/{actualvideo}") # Delete the old video
    
    print("TRIM COMPLETE")
    print("Extracted files in /tmp:", os.listdir("/tmp"))
    print("STARTING UPLOAD")

    with TelegramClient('/tmp/anoni.session', api_id, api_hash) as client:
        client.loop.run_until_complete(client.send_file('+**********', f"/tmp/trim_{actualvideo}", chunk_size=10 * 1024 * 1024, caption=f"{video_url}")) # Upload the video
        
    print("UPLOAD COMPLETE")
    
    return {
        'statusCode': 200,
        'body': json.dumps('UPLOAD COMPLETE')
    }
