from os.path import exists
from re import match
from json import dump, load
from functions import  play_video, search_download, url_download

YOUTUBE_REGEX = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'

with open('settings.json') as f:
    settings = load(f)


if selected_video := input("\n\n\nFILENAME, YOUTUBE URL, OR YOUTUBE SEARCH: "):
    write_audio = True
    if exists(selected_video):
        settings['lastVideo'] = video_name = selected_video
    else:
        settings['lastVideo'] = video_name = 'video.mp4'
        if match(YOUTUBE_REGEX, selected_video):
            url_download(selected_video)
        else:
            search_download(selected_video)
    with open('settings.json', 'w') as f:
        dump(settings, f)
else:
    write_audio = False
    video_name = settings['lastVideo']


play_video(video_name, settings['height'], write_audio=write_audio)