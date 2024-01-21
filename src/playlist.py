import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('You-Tube-API')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, _id) -> None:
        self._id = _id
        playlist_info = youtube.playlists().list(id=self._id, part='snippet').execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self._id}'

    @property
    def total_duration(self):
        videos = youtube.playlistItems().list(playlistId=self._id, part='contentDetails').execute()
        total_duration_seconds = 0
        for video in videos['items']:
            video_id = video['contentDetails']['videoId']
            video_info = youtube.videos().list(part='contentDetails', id=video_id).execute()
            iso_8601_duration = video_info['items'][0]['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration_seconds += duration.total_seconds()

        total_duration = timedelta(seconds=total_duration_seconds)
        return total_duration

    def show_best_video(self):
        videos = youtube.playlistItems().list(playlistId=self._id, part='contentDetails').execute()
        video_likes = {}
        for video in videos['items']:
            video_id = video['contentDetails']['videoId']
            video_info = youtube.videos().list(part='statistics', id=video_id).execute()
            likes = int(video_info['items'][0]['statistics']['likeCount'])
            video_likes[video_id] = likes

        max_key = max(video_likes, key=video_likes.get)
        return f'https://youtu.be/{max_key}'