from os import chdir, mkdir, getcwd, get_terminal_size, system
from os.path import exists, isdir
from re import match
from json import dump, load
from functions import play_video, get_custom_name, search_video, url_download, url_video
from typing import Optional
from pygame import mixer
from pyfiglet import figlet_format
YOUTUBE_REGEX = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
UNACCEPTABLE_FILE_CHARS = '\\/:*?"<>|'

def file_name_convert(name: str):
    return 'Downloads/' + ''.join(char for char in name if char not in UNACCEPTABLE_FILE_CHARS)

def main(forced_load: Optional[bool] = None):
    with open('settings.json') as f:
        settings = load(f)
        last_video = settings['lastVideo']
    video_name = 'video.mp4'

    forced_load = last_video if forced_load else forced_load

    selected_video = settings['lastVideo'] = forced_load or input("\n\n\nFILENAME, YOUTUBE URL, OR YOUTUBE SEARCH: ") or last_video
    height = get_terminal_size().lines  # autoresize
    with open('settings.json', 'w') as f:
        dump(settings, f, indent=4)

    if exists(selected_video):
        video_name = selected_video
    else:
        if isdir(selected_video):
            chdir(selected_video)
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
            video_dir = file_name_convert(custom_name)
            if isdir(video_dir):
                chdir(video_dir)
            else:
                mkdir(video_dir)
                chdir(video_dir)
                print("Downloading youtube video...")
                url_download(url)
                print("Done!")
    return play_video(
        video_name,
        height-1,
        not exists('audio.mp3'),
    )

if __name__ == '__main__':
    default_path = getcwd()
    response = None
    print(figlet_format("THIS IS A TEXT TEST", font='doh', width=get_terminal_size().columns))
    while True:
        try:
            response = main(response)
        except KeyboardInterrupt:
            response = None
        except IndexError:
            input("The search encountered an extreme error. Please try a different search...")
            response = None
        mixer.music.unload()
        system('cls')
        chdir(default_path)