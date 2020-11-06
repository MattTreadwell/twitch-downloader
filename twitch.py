#!/usr/bin/python3

import requests
import json
import sys

PREVIEW_IMG_KEY = "thumbnail_url"

def get_data(url):
    print("Sending GET request to " + url)
    r = requests.get(url, headers = {'User-agent': 'Twitch Clip Downloader'})
    print("Status Code: " + str(r.status_code))
    return r.json()


def extract_key_val(data, key):
    ret_val = []
    
    if (isinstance(data, list)):
        for i in data:
            ret_val += extract_key_val(i, key)
    elif (isinstance(data, dict)):
        for k in data.keys():
            if k == PREVIEW_IMG_KEY:
                ret_val.append(data[k])
            else:
                ret_val += extract_key_val(data[k], key)

    return ret_val

def urls_prev_to_mp4(urls):
    ret_val = []

    for u in urls:
        ret_val.append(u[:len(u)-12] + ".mp4")

    return ret_val


def get_filename(reddit_url):
    s = sys.argv[1][:len(sys.argv[1])-1].split('/')
    filename = s[-1] + ".mp4"
    return filename



def attempt_download(urls, filename):
    for u in urls:
        print("Attempting download of", u)
        r = requests.get(u, allow_redirects=True)
        print("Status Code: " + str(r.status_code))
        if r.status_code == 200:
            open(filename, 'wb').write(r.content)
            print("File downloaded to:", filename)
            return
 

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./twitch.py [REDDIT_POST_URL]")
        exit(3)
    reddit_url = sys.argv[1]
    reddit_url = reddit_url[:len(reddit_url)-1] + ".json"
    reddit_json = get_data(reddit_url)
    key_matches = extract_key_val(reddit_json, PREVIEW_IMG_KEY)
    video_urls = urls_prev_to_mp4(key_matches)
    print("Potential links:", key_matches)
    filename = get_filename(sys.argv[1])
    attempt_download(video_urls, filename)

