from Cache_Manager import Video_Cache_Manager
from Structs import *
from enum import Enum
import time
from omxplayer.player import OMXPlayer

# TRIAL FOR OMX PLAYER
from pathlib import Path
from time import sleep


STATIC_VIDEO_PATH = Path("./stock/static_low_1.mp4")

class Status(Enum):
    IDLE = 0
    PLAYING = 1
    DOWNLOADING = 2

class Operating_Context:
    def __init__(self, status=Status.IDLE, cache_manager=Video_Cache_Manager(), cur_video=None, load_manager=False):
        self.status=status
        if load_manager:
            self.cache_manager = Video_Cache_Manager.load()
        else:
            self.cache_manager = cache_manager
        self.cur_video = cur_video
        self.seen_videos = set()

        self.player = None

def reload_playlist(context, videos_per_channel=5):
    context.cache_manager.clear_all()
    channels = [Channel(x, video_limit=videos_per_channel) for x in config.CHANNEL_LIST]
    # print(channels)
    for channel in channels:
        videos = channel.videos
        for video in videos:
            # If the video is not in queue or in seen videos, queue it up
            if video not in context.seen_videos and not context.cache_manager.video_in_queue(video):
                context.cache_manager.add_video(video, video.published_date)
                print("added video ", context.cache_manager.queue_size())

def downloading(context, videos_predownloaded = 3):
    context.status = Status.DOWNLOADING
    top_n_videos = [context.cache_manager.pop_video(x) for x in range(videos_predownloaded)]
    for video in top_n_videos:
        if video != None:
            video.download()
            context.cache_manager.add_video(video, video.published_date)

    playing(context)


def playing(context):
    context.status = Status.PLAYING
    cur_video = context.cache_manager.peek_video()


    if cur_video.is_ready():
        play_context_video(context, video_path=cur_video.disk_path)
    else:
        print("VIDEO IS NOT READY U BUM")


def quit_context_player(context):
    if context.player != None:
        context.player.quit()

def play_context_video(context, video_path):
    quit_context_player(context)
    context.player = OMXPlayer(video_path)
    # context.player.set_aspect_mode('stretch')
    context.player.play()
    context.player.play()


def idling(context, guaranteed_videos=5):
    context.status = Status.IDLE
    print("IDLING, finding videos to watch")

    play_context_video(context, STATIC_VIDEO_PATH)

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
                print("Waiting {} seconds to fetch new videos".format(retry_wait))
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
    context = Operating_Context(load_manager=True)
    print(context.seen_videos)
    if context.status == Status.IDLE:
        idling(context)
