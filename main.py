from os import chdir, mkdir
from os.path import exists, isdir
from re import match
from json import dump, load
from functions import play_video, get_custom_name, search_video, url_download, url_video

YOUTUBE_REGEX = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'

with open('settings.json') as f:
    settings = load(f)
    last_video = settings['lastVideo']
    HEIGHT = settings['height']
video_name = 'video.mp4'

selected_video = settings['lastVideo'] = input("\n\n\nFILENAME, YOUTUBE URL, OR YOUTUBE SEARCH: ") or last_video
with open('settings.json', 'w') as f:
    dump(settings, f, indent=4)

if exists(selected_video):
    video_name = selected_video
else:
    if isdir(video_dir := 'Downloads\\' + selected_video):
        chdir(video_dir)
    else:
        print("Fetching youtube video...")
        if match(YOUTUBE_REGEX, selected_video):
            video = url_video(selected_video)
            url = selected_video
        else:
            video = search_video(selected_video)
            url_suffix = video.to_dict(clear_cache=False)[0]['url_suffix']
            url = 'https://www.youtube.com' + url_suffix
        print("Done!")
        custom_name = get_custom_name(video)
        video_dir = 'Downloads\\' + custom_name
        if isdir(video_dir):
            chdir(video_dir)
        else:
            mkdir(video_dir)
            chdir(video_dir)
            print("Downloading youtube video...")
            url_download(url)
            print("Done!")

play_video(video_name, HEIGHT, write_audio=not exists('audio.mp3'))