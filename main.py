from Cache_Manager import Video_Cache_Manager
from Structs import *
from enum import Enum
import time

class Status(Enum):
    IDLE = 0
    PLAYING = 1
    DOWNLOADING = 2

class Operating_Context:
    def __init__(self, status=Status.IDLE, cache_manager=Video_Cache_Manager(), cur_video=None):
        self.status=status
        self.cache_manager = cache_manager
        self.cur_video = cur_video
        self.seen_videos = set()

def reload_playlist(context, videos_per_channel=5):
    context.cache_manager.clear_all()
    channels = [Channel(x, video_limit=videos_per_channel) for x in config.CHANNEL_LIST]
    for channel in channels:
        videos = channel.videos
        for video in videos:
            # If the video is not in queue or in seen videos, queue it up
            if video not in context.seen_videos and video not in context.cache_manager.video_in_queue(video):
                context.cache_manager.add_video(video)

def downloading(context, videos_predownloaded = 3):
    context.status = Status.DOWNLOADING
    top_n_videos = [context.cache_manager.pop(x) for x in range(videos_predownloaded)]
    for video in top_n_videos:
        if video != None:
            video.download()
            context.cache_manager.add_video(video, video.published_date)

    playing(context)


def playing(context):
    context.status = Status.PLAYING
    cur_video = context.cache_manager.peek_video()
    if cur_video.is_ready():

    else:

def idling(context, guaranteed_videos=5):
    context.status = Status.IDLE
    print("IDLING, finding videos to watch")

    if not context.cache_manager.queue_size() >= guaranteed_videos:
        num_videos = 5
        retry = True
        # Exponential wait
        retry_wait = 2
        while retry:
            reload_playlist(context=context, videos_per_channel=num_videos)
            if context.cache_manager.queue_size() >= guaranteed_videos:
                retry = False
            else:
                print("Waiting {} seconds to fetch new videos")
                time.sleep(retry_wait)
                retry_wait **= 2
                num_videos += 5
    downloading(context)

if __name__ == "__main__":
    # Random test
    # status = Status.IDLE
    # cache_manager = Video_Cache_Manager()
    # print(cache_manager.__dict__)
    # c = Channel(config.CHANNEL_LIST[0], video_limit=3)
    # c.download_videos()
    # for video in c.videos:
    #     date = datetime.datetime.strptime(video.published_date, "%Y-%m-%dT%H:%M:%S")
    #     cache_manager.add_video(video, date)
    #
    # while cache_manager.data_struct.size() > 0:
    #     cur_video = cache_manager.pop_video(delete=True)
    #     print(cur_video.name)
    context = Operating_Context()
    if context.status == Status.IDLE:
        idling(context)
