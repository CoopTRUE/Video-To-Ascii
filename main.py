from typing import Optional
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from os import chdir, mkdir, getcwd, get_terminal_size, system, startfile
from shutil import rmtree
from os.path import exists, isdir
from re import match
from json import dump, load
from moviepy.editor import VideoFileClip
from functions import play_video, get_custom_name, search_video, url_download, url_video
from pygame import mixer
from pyfiglet import figlet_format
from time import time
# So many imports oh my god

YOUTUBE_REGEX = '^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
UNACCEPTABLE_FILE_CHARS = '\\/:*?"<>|'
DEFAULT_PATH = getcwd()
# TEMPLATES:
# Dark -> Light
# " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" 3.69
# ░▒█
# "@%#*+=-:. " 42.51

def file_name_convert(name: str) -> str:
    """Returns a proper folder folder name for a folder with the name `name`."""
    return ''.join(char for char in name if char not in UNACCEPTABLE_FILE_CHARS)

def main(forced_load: Optional[bool] = None):
    """Main function for Video-To-Ascii. Forced load forces the input to be whatever is passed. Returns the reponse."""

    # Load json settings
    with open('settings.json') as f:
        settings = load(f)
        ascii_chars = settings['asciiChars']
        reverse = settings['reverse']
        prioritize = settings['prioritize']
        buffer_delay = settings['bufferDelay']
        pixel_width = settings['pixelWidth']
        side_by_side_comparison = settings['sideBySideComparison']
        last_video = settings['lastVideo']
        threads = settings['threads']
        # TEMPORARY FAST FORWARD REMOVE
        # fast_forward = settings['fastForward']

    # If reverse reverse the ascii characters variable and the ascii characters within the json file
    if reverse:
        ascii_chars = settings['asciiChars'] = ascii_chars[::-1]
        settings['reverse'] = reverse = False

    # Extreme logic shit some of you can't handle
    selected_video = settings['lastVideo'] = (
        last_video if forced_load else forced_load
        or input("\n\n\nFILENAME, FOLDER NAME, YOUTUBE URL, OR YOUTUBE SEARCH: ")
        or last_video
    )
    # Seriously though this is some real optimization

    # TEMPORARY FAST FORWARD REMOVE
    # settings['fastForward'] = 0

    # Dump override the 'settings.json' regardless of whether settings was actually changed
    with open('settings.json', 'w') as f:
        dump(settings, f, indent=4)

    video_name = 'video.mp4'

    if exists(selected_video):  # If video is literally a video file in the Video-To-Ascii directory
        video_name = selected_video
    else:
        chdir('Downloads')
        if isdir(selected_video):  # If an actual video directory is inputted then use it
            chdir(selected_video)
        else:  # Must be a youtube video search or url
            print("Fetching youtube video...")
            if match(YOUTUBE_REGEX, selected_video):  # If input is a youtube url
                video = url_video(selected_video)
                url = selected_video
            else:
                video = search_video(selected_video)
                url_suffix = video.to_dict(clear_cache=False)[0]['url_suffix']
                url = 'https://www.youtube.com' + url_suffix
            # url should be the youtube video url
            print("Done!")
            custom_name = get_custom_name(video)  # Get special name based off of video id and title
            video_dir = file_name_convert(custom_name)  # Get folder name adjusted to be allowed to be created on windows at least
            if isdir(video_dir):  # If the folder already exists meaning the video has already been downloaded
                chdir(video_dir)
            else:
                mkdir(video_dir)  # Make the directory
                chdir(video_dir)
                print("Downloading youtube video...")
                try:
                    url_download(url)  # Actually download the video
                except KeyboardInterrupt:  # If the users wants to stop downloading
                    print("Aborting...")
                    chdir(DEFAULT_PATH + "/Downloads")
                    rmtree(video_dir)
                    return
                print("Done!")

    audio_name = 'audio.mp3'
    if not exists(audio_name):  # If audio hasn't already been written
        print(f"Witing audio file {audio_name}...")
        with VideoFileClip(video_name) as video:
            video.audio.write_audiofile(audio_name)
        print("Done!")

    # If you want a side by side comparison
    if side_by_side_comparison:
        startfile(video_name)

    vidcap = VideoCapture(video_name)
    video_width = vidcap.get(CAP_PROP_FRAME_WIDTH)
    video_height = vidcap.get(CAP_PROP_FRAME_HEIGHT)


    if not video_width:  # video_width will be None if the file isn't fully donwloaded
        new_dir, _, delete_dir = getcwd().rpartition('\\')
        full_name = delete_dir[delete_dir.index(' ')+1:]
        print(f"Video file '{full_name}' isn't fully downloaded.")
        if input(f"Would you like to delete the video folder '{delete_dir}' and redownload? (y/n): ") == 'y':
            chdir(new_dir)
            print(f"Deleting {delete_dir}...")
            rmtree(delete_dir)
            return True
        return

    frame_rate = vidcap.get(CAP_PROP_FPS)

    height = get_terminal_size().lines-1

    # If the video should be in the correct ratio or in the width
    # If the video width is longer than the terminal then default to the terminal width
    terminal_width = get_terminal_size().columns-10
    if prioritize == 'max':
        width = terminal_width
    else:
        width = min(terminal_width, int(video_width//(video_height/height))*2)

    # Run the video until it is over or the user pressed ctrl + C
    try:
        # temp_time = time()
        play_video(
            vidcap,
            audio_name,
            width,
            height,
            ascii_chars,
            pixel_width,
            buffer_delay,
            frame_rate,
            threads
            # fast_forward
        )
    # TEMPORARY FAST FORWARD REMOVE
        """
        return play_video(
            vidcap,
            audio_name,
            width,
            height,
            ascii_chars,
            pixel_width,
            buffer_delay,
            frame_rate,
            # fast_forward
        ), (time() - temp_time) * frame_rate
        """
    except KeyboardInterrupt:
        # Exist side by side comparison video file if it was ever opened
        if side_by_side_comparison: system('taskkill /im Video.UI.exe /f')
        # TEMPORARY FAST FORWARD REMOVE
        # return None, (time() - temp_time) * frame_rate


if __name__ == '__main__':
    response = None
    mixer.init()


    print(figlet_format("THIS IS A TEXT TEST", font='doh', width=get_terminal_size().columns))
    while True:
        # response, fast_forward = main(response)
        response = main(response)
        mixer.music.unload()
        system('cls')
        chdir(DEFAULT_PATH)
        # TEMPORARY FAST FORWARD REMOVE
        """
        with open('settings.json', 'r') as f:
            settings = load(f)
        settings['fastForward'] = fast_forward
        with open('settings.json', 'w') as f:
            dump(settings, f, indent=4)
        """