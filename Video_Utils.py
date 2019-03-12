from __future__ import unicode_literals

import subprocess
import youtube_dl


class Callback:
    def _init__(self):
        pass

    def run(self, data):
        return

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def NULL_FUNCTION(d):
    pass

# File format
# 'temp/%(title)s-%(id)s.%(ext)s'
def download_video(url, output_dir= "temp", callback = Callback()):
    def finished_downloading_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
            callback.run(d)
    ydl_opts = {
        'format': "135",
        'logger': MyLogger(),
        'progress_hooks': [finished_downloading_hook],
        'outtmpl': output_dir + '/%(id)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


