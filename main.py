from Cache_Manager import Video_Cache_Manager
from Structs import *
from enum import Enum
class Status(Enum):
    IDLE = 0
    PLAYING = 1
    DOWNLOADING = 2

class Operating_Context:
    def __init__(self, status=None, cache_manager=None, cur_video=None):
        self.status=status
        self.cache_manager = cache_manager
        self.cur_video = cur_video

def reload_playlist(cache_manager):
    cache_manager.
# def idling(context):





if __name__ == "__main__":
    status = Status.IDLE
    cache_manager = Video_Cache_Manager()
    print(cache_manager.__dict__)
    c = Channel(config.CHANNEL_LIST[0], video_limit=3)
    c.download_videos()
    for video in c.videos:
        date = datetime.datetime.strptime(video.published_date, "%Y-%m-%dT%H:%M:%S")
        cache_manager.add_video(video, date)

    while cache_manager.data_struct.size() > 0:
        cur_video = cache_manager.pop_video(delete=True)
        print(cur_video.name)






