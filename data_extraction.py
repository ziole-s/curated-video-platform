import requests
import json
from urllib.parse import urlparse, parse_qs
import os

API_KEY = 'AIzaSyA51jVRxV2WNbT-oLtCCY5ZJ7GGMwMO0eY'  # Replace this with your real API key


def get_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname in ('youtu.be', 'www.youtu.be'):
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None


def fetch_video_info(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch video info for ID: {video_id}")
        return None

    data = response.json()
    items = data.get('items')
    if not items:
        print(f"No video info found for ID: {video_id}")
        return None

    snippet = items[0]['snippet']
    title = snippet['title']
    thumbnails = snippet['thumbnails']
    thumbnail_url = thumbnails.get('medium', thumbnails.get('default', {})).get('url', '')
    return {
        'title': title,
        'thumbnailURL': thumbnail_url,
        'videoURL': f'https://www.youtube.com/watch?v={video_id}'
    }


def append_videos_to_json(file_path, video_urls):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    for url in video_urls:
        video_id = get_video_id(url)
        if not video_id:
            print(f"Skipping invalid URL: {url}")
            continue
        info = fetch_video_info(video_id)
        if info:
            existing_data.append(info)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2)

    print(f"Appended {len(video_urls)} videos to {file_path}")


if __name__ == "__main__":
    category = input("enter category name")
    video_list = [

    ]

    append_videos_to_json(f'video_base/{category}_category.json', video_list)
