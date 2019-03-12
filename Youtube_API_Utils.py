import requests
import config
import pprint

CHANNELS_ENDPOINT = "https://www.googleapis.com/youtube/v3/channels"
PLAYLIST_ITEMS_ENDPOINT = "https://www.googleapis.com/youtube/v3/playlistItems"

pp = pprint.PrettyPrinter(indent=4)

def fetch_channel_information(channel_id):
    params = {"part" : "contentDetails",
              "id" : channel_id,
              "key" : config.YOUTUBE_DATA_API_KEY}
    res = requests.get(CHANNELS_ENDPOINT, params)
    if res.status_code != 200:
        raise Exception("Something went wrong with the request: " + res.json())

    return res.json()


def fetch_videos_from_playlist(playlist_id, max_results = 10):
    params = {"part": "snippet,contentDetails",
              "playlistId": playlist_id,
              "maxResults":max_results,
              "key": config.YOUTUBE_DATA_API_KEY}

    res = requests.get(PLAYLIST_ITEMS_ENDPOINT, params)
    # pp.pprint(res.json()['items'])
    if res.status_code != 200:
        raise Exception("Something went wrong with the request: " + res.json())

    vid_list = []
    for item in res.json()["items"]:
        vid_list.append({"id" : item["contentDetails"]["videoId"],
                         "title" : item["snippet"]["title"],
                         "published" : item["contentDetails"]["videoPublishedAt"]})

    return vid_list


fetch_videos_from_playlist('UU6107grRI4m0o2-emgoDnAA')








