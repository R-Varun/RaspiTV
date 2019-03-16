import config
import datetime
from pathlib import Path
from Video_Utils import download_video, Callback
from Youtube_API_Utils import fetch_videos_from_playlist, fetch_channel_information


class Video_Downloaded_Callback(Callback):
    def __init__(self, video_obj):
        self.video_obj = video_obj
    #overrides
    def run(self, data):
        self.video_obj.ready = True
        self.video_obj.set_disk_path(data["filename"])

class Video:
    def __init__(self, name, id, ready = False, published_date = None, channel_id=None, disk_path=None):
        self.name = name
        self.id = id
        self.url = self.url_from_id(id)
        self.ready = ready

        self.published_date = published_date
        self.channel_id = channel_id

        if disk_path != None:
            self.disk_path = Path(disk_path)
        else:
            self.disk_path = None

    @staticmethod
    def url_from_id(video_id):
        return "https://www.youtube.com/watch?v={}".format(video_id)

    def is_ready(self):
        return self.ready

    def set_disk_path(self, disk_path):
        self.disk_path = Path(disk_path)

    def download(self):
        if not self.ready:
            download_video(self.url, config.VIDEO_CACHE_DIR, Video_Downloaded_Callback(self))
        else:
            print("Video has been ready!")

    def __repr__(self):
        return "Video Object    Title:{}   ID:{}    IS READY:{}".format(self.name, self.id, self.is_ready())

    def __cmp__(self, other):
        return hash(self) - hash(other)

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    # This shit suck
    # def __hash__(self):
    #     return (self.id, self.name)
class Channel:
    def __init__(self, channel_id, video_limit=10, update_videos=True):
        self.channel_id = channel_id
        channel_details = fetch_channel_information(self.channel_id)
        self.uploads_playlist_id = channel_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        self.videos = []
        self.video_limit = video_limit
        self.last_updated = None
        if update_videos:
            self.update_videos()

    def update_videos(self):
        data = fetch_videos_from_playlist(self.uploads_playlist_id,  max_results=self.video_limit)
        self.videos = []
        for item in data:
            date = item["published"]
            formatted_date = date[:date.index(".")]
            video = Video(name=item["title"],id=item["id"], published_date=formatted_date, channel_id=self.channel_id)
            self.videos.append(video)

        self.last_updated = datetime.datetime.now()

    def download_videos(self):
        for video in self.videos:
            print("set dl")
            video.download()


if __name__ == "__main__":
    c = Channel("UC1ZBQ-F-yktYD4m5AzM6pww", video_limit=3)

    print(c.channel_id)
    print(c.videos)
    print(c.last_updated)
    print(len(c.videos))
    c.download_videos()
    print(c.videos)
