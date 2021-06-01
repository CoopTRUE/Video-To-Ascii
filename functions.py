from time import sleep, time
from PIL import Image
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from pytube import YouTube
from youtube_search import YoutubeSearch
from typing import Optional, Sequence, Union
from moviepy.editor import VideoFileClip
from pygame import mixer
from pyfiglet import figlet_format
from os import get_terminal_size
from os import getcwd, chdir
from shutil import rmtree

mixer.init()
def convert_data(image_data: Sequence[Sequence[Sequence[int]]], resize: Optional[Sequence[int]] = None) -> str:
    """Convert image data into ASCII text and optional resizes the image. Returns the ASCII text"""
    ASCII_CHARS = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
    PIXEL_WIDTH = 3.69

    image_data = Image.fromarray(image_data)
    if resize:
        image_data = image_data.resize((resize))
        WIDTH = resize[0]
    else:
        WIDTH = len(image_data[0])
    image_data = image_data.convert('L')
    image_data = image_data.getdata()

    new_data = [ASCII_CHARS[int(pixel_value/PIXEL_WIDTH)] for pixel_value in image_data]
    length = len(new_data)
    split_data = [''.join(new_data[index: index+WIDTH]) for index in range(0, length, WIDTH)]
    return '\n'.join(split_data)

def url_download(url: str) -> YouTube:
    """Download the youtube video at the url. Returns the YouTube object."""
    yt = url_video(url)
    streams = yt.streams
    stream = streams.first()
    stream.download(filename='video')
    return yt

# def search_download(video_name: str):
#     """Search youtube for the video name and download the first video. Returns the video ID."""
#     url_suffix = search(video_name, remove_prefix=False)
#     url = 'https://www.youtube.com' + url_suffix
#     return url_download(url)
#     # search = YoutubeSearch(video_name, max_results=1)
#     # url_suffix = search.to_dict()[0]['url_suffix']
#     # url = 'https://www.youtube.com' + url_suffix
#     # url_download(url)
#     # return url_suffix.removeprefix('/watch?v=')

def get_custom_name(youtube_object: Union[YouTube, YoutubeSearch]) -> str:
    if isinstance(youtube_object, YouTube):
        id = youtube_object.video_id
        title = youtube_object.title
    elif isinstance(youtube_object, YoutubeSearch):
        video_dict = youtube_object.to_dict()[0]
        id = video_dict['id']
        title = video_dict['title']
    else:
        raise TypeError
    print(figlet_format(title, font='doh', width=get_terminal_size().columns))
    custom_name = id + ' ' + title
    return custom_name


def url_video(url: str) -> YouTube:
    return YouTube(url)

def search_video(video_name: str) -> YoutubeSearch:
    return YoutubeSearch(video_name, max_results=1)

def search(video_name: str) -> dict:
    """Search youtube for the video name. Return the properties of the first video."""
    search = YoutubeSearch(video_name)
    search_dict = search.to_dict()
    return search_dict[0]

def play_video(name: str, size: int, write_audio: bool = True, frame_rate: Optional[Union[float, int]] = None):
    # WIDTH = size[0]
    HEIGHT = size
    vidcap = VideoCapture(name)
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
    WIDTH = int(video_width//(video_height/HEIGHT))*2

    FRAME_RATE = frame_rate or vidcap.get(CAP_PROP_FPS)
    FRAME_RATE = 1/FRAME_RATE

    audio_name = 'audio.mp3'
    # # if not exists(audio_name):

    if write_audio:
        print(f"Witing audio file {audio_name}...")
        with VideoFileClip(name) as video:
            video.audio.write_audiofile(audio_name)
        print("Done!")

    mixer.music.load(audio_name)
    success, frame = vidcap.read()

    mixer.music.play()

    time_buffer = 0
    while success:
        old_time = time()
        text = convert_data(frame, (WIDTH, HEIGHT))
        print(chr(27))
        print(text, flush=True)
        success, frame = vidcap.read()   #Read frame
        time_buffer = time_buffer + (FRAME_RATE - (time() - old_time))
        if time_buffer > .06:
            sleep(.06)
            time_buffer = time_buffer - .06