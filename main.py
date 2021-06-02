from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from os import chdir, mkdir, getcwd, get_terminal_size, system
from shutil import rmtree
from os.path import exists, isdir
from re import match
from json import dump, load

from numpy.lib.function_base import select
from functions import play_video, get_custom_name, search_video, url_download, url_video
from typing import Optional
from pygame import mixer
from pyfiglet import figlet_format
YOUTUBE_REGEX = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
UNACCEPTABLE_FILE_CHARS = '\\/:*?"<>|'

def file_name_convert(name: str):
    return 'Downloads/' + ''.join(char for char in name if char not in UNACCEPTABLE_FILE_CHARS)

def main(forced_load: Optional[bool] = None):
    response = input("\n\n\nFILENAME, YOUTUBE URL, OR YOUTUBE SEARCH: ")

    with open('settings.json') as f:
        settings = load(f)
        ascii_chars = settings['asciiChars']
        prioritize = settings['prioritize']
        buffer_delay = settings['bufferDelay']
        side_by_side_comparison = settings['sideBySideComparison']
        last_video = settings['lastVideo']

    selected_video = settings['lastVideo'] = (
        (last_video if forced_load else forced_load)
        or response
        or last_video
    )

    video_name = 'video.mp4'

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

    vidcap = VideoCapture(video_name)
    video_width = vidcap.get(CAP_PROP_FRAME_WIDTH)

    if not video_width:
        new_dir, _, delete_dir = getcwd().rpartition('\\')
        full_name = delete_dir[delete_dir.index(' ')+1:]
        print(f"Video file '{full_name}' isn't fully downloaded.")
        if input(f"Would you like to delete the video folder '{delete_dir}' and redownload? (y/n): ") == 'y':
            chdir(new_dir)
            print(f"Deleting {delete_dir}...")
            rmtree(delete_dir)
            return True
        return

    video_height = vidcap.get(CAP_PROP_FRAME_HEIGHT)

    if PRIORITIZE == 'max':
        width = get_terminal_size().columns-10
    else:
        width = int(video_width//(video_height/height))*2

    FRAME_RATE = frame_rate or vidcap.get(CAP_PROP_FPS)
    FRAME_RATE = 1/FRAME_RATE

    audio_name = 'audio.mp3'
    # # if not exists(audio_name):

    if write_audio:
        print(f"Witing audio file {audio_name}...")
        with VideoFileClip(name) as video:
            video.audio.write_audiofile(audio_name)
        print("Done!")

    if SIDE_BY_SIDE_COMPARISON:
        startfile(name)
    mixer.music.load(audio_name)
    mixer.music.play()
    success, frame = vidcap.read()

    buffer = 0

    while success:
        old_time = perf_counter()
        text = convert_data(frame, (width, height))
        print(chr(27))
        print(text)
        success, frame = vidcap.read()   #Read frame
        if not BUFFER_DELAY:
            continue
        buffer = buffer + (FRAME_RATE - (perf_counter() - old_time))
        if buffer >= BUFFER_DELAY:
            sleep(BUFFER_DELAY)
            buffer = buffer - BUFFER_DELAY

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