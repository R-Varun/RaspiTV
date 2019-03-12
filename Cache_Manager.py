import pickle
from pathlib import Path
import heapq
import os
import datetime
import config
from Video_Utils import *


class PQ:
    def __init__(self):
        self.back = []
        heapq.heapify(self.back)

    def push(self, item, priority):
        print(self.back, item, priority)
        heapq.heappush(self.back, (priority, item))

    def pop(self):
        return heapq.heappop(self.back)[1]

    def pop_with_priority(self):
        popped = heapq.heappop(self.back)
        return popped[::-1]

    def size(self):
        return len(self.back)

class Video_Cache_Manager:
    def __init__(self, save_dir="/cache_manager", size_limit=4):
        self.save_dir = Path(save_dir)

        self.cache_dir = Path(config.VIDEO_CACHE_DIR)
        if not self.cache_dir.exists():
            os.mkdir(self.cache_dir)
        self.data_struct = PQ()
        self.data_struct_exists = set()


    def add_and_download_video(self, video, priority=None):
        video.download()
        self.add_video(video, priority=priority)
    # Default add
    def add_video(self, video, priority=None):
        assert(video.disk_path.exists())

        if priority == None:
            priority = datetime.datetime.now()
        print(self.data_struct)
        self.data_struct.push(video, priority)
        self.data_struct_exists.add(video)

    def pop_video(self, delete=False):
        video = self.data_struct.pop()
        self.data_struct_exists.remove(video)
        if delete:
            self.delete_video_from_disk(video)
        return video

    @staticmethod
    def delete_video_from_disk(video):
        disk_location = video.disk_path
        if disk_location == None:
            print("Video disk location never set!")
            return
        if disk_location.exists():
            os.remove(disk_location)
        else:
            print("Disk location not found!")

    def default_generate_video_name_cache(self, video):
        return video.name + ""

    def num_videos(self):
        return self.data_struct.size()

    def save(self):
        with open(self.save_dir) as file:
            pickle.dump(self, file)

    # Deletes all disk items and clears in-memory data structures
    def clear_all(self):
        self.data_struct = PQ()
        for video in self.data_struct_exists:
            self.delete_video_from_disk(video)
        self.data_struct_exists = set()

if __name__ == "__main__":
    c = Video_Cache_Manager()
    print(vars(c))