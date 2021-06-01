from os import chdir, mkdir
from os.path import exists, isdir
from re import match
from json import dump, load
from functions import search, play_video, get_custom_name, url_download
from pytube import YouTube

YOUTUBE_REGEX = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'

with open('settings.json') as f:
    settings = load(f)
    last_video = settings['lastVideo']
    write_audio = False

if selected_video := input("\n\n\nFILENAME, YOUTUBE URL, YOUTUBE SEARCH, OR 'ENTER' KEY FOR LAST VIDEO: "):
    if isdir(download_dir := 'Downloads\\' + selected_video):
        chdir(download_dir)
    elif exists(selected_video):
        pass
    elif match(YOUTUBE_REGEX, selected_video):
        custom_name = video
        custom_name = get_custom_name(selected_video)
        video_dir = 'Downloads\\' + custom_name
        if isdir(video_dir):
            chdir(download_dir)
        else:
            mkdir(video_dir)
            chdir(video_dir)
    else:
        custom_name = get_custom_name(selected_video)
        video_dir = 'Downloads\\' + custom_name
        if isdir(video_dir):
            chdir(download_dir)
        else:
            mkdir(video_dir)
            chdir(video_dir)
write_audio = not exists('audio.mp3')

# if selected_video := input("\n\n\nFILENAME, YOUTUBE URL, OR YOUTUBE SEARCH: "):
#     write_audio = True
#     if exists(selected_video):
#         if settings['lastVideo'] == selected_video:
#             write_audio = False
#         settings['lastVideo'] = video_name = selected_video
#     else:
#         settings['lastVideo'] = video_name = 'video.mp4'
#         if match(YOUTUBE_REGEX, selected_video):
#             url_download(selected_video)
#         else:
#             search_download(selected_video)
#     with open('settings.json', 'w') as f:
#         dump(settings, f, indent=4)
# else:
#     write_audio = False
#     video_name = settings['lastVideo']

# try:
#     play_video(video_name, settings['height'], write_audio=write_audio)
# except Exception as e:
#     input()