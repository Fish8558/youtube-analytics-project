import json
import os

from googleapiclient.discovery import build

API_KEY = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.set_attributes()

    def set_attributes(self) -> None:
        """Атрибуты экзепляра"""
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id,
                                               part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        """Сохранение данных в json"""
        data = {
            "id канала": self.__channel_id,
            "Название канала": self.title,
            "Описание канала": self.description,
            "ссылка на канал": self.url,
            "количество подписчиков": self.subscriber_count,
            "количество видео": self.video_count,
            "общее количество просмотров": self.view_count
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
