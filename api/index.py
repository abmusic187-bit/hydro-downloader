from fastapi import FastAPI, HTTPException
import yt_dlp
import os
from supabase import create_client

app = FastAPI()

# Connect to Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/api/extract")
def extract_video(url: str):
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info.get('url')
            title = info.get('title')

            # Log to Supabase Database
            supabase.table("downloads").insert({"title": title, "video_url": url}).execute()

            return {"status": "success", "download_url": download_url, "title": title}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
