from time import sleep, time
from PIL import Image
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from pytube import YouTube
from youtube_search import YoutubeSearch
from typing import Optional, Sequence, Union, Any
import moviepy.editor as mp
from json import load, dump
# from os.path import exists
from playsound import playsound
import threading


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

def url_download(url: str) -> str:
    """Download the youtube video at the url. Returns the video ID."""
    yt = YouTube(url)
    streams = yt.streams
    stream = streams.first()
    stream.download(filename='video')
    return url.split('/watch?v=')[1][:11]

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

def get_custom_name(url: str) -> str:
    video_dict = search(video_name)
    custom_name = video_dict['id'] + ' ' + video_dict['title']
    return custom_name

def search(video_name: str) -> dict:
    """Search youtube for the video name. Return the properties of the first video."""
    search = YoutubeSearch(video_name)
    search_dict = search.to_dict()
    return search_dict[0]


def play_video(name: str, size: int, frame_rate: Optional[Union[float, int]] = None, write_audio: bool = True):
    # WIDTH = size[0]
    HEIGHT = size
    vidcap = VideoCapture(name)

    video_width = vidcap.get(CAP_PROP_FRAME_WIDTH)
    video_height = vidcap.get(CAP_PROP_FRAME_HEIGHT)
    WIDTH = int(video_width//(video_height/HEIGHT))*2

    FRAME_RATE = frame_rate or vidcap.get(CAP_PROP_FPS)
    FRAME_RATE = 1/FRAME_RATE

    audio_name = 'audio.mp3'
    # # if not exists(audio_name):
    if write_audio:
        with mp.VideoFileClip(name) as video:
            video.audio.write_audiofile(audio_name)

    success, frame = vidcap.read()
    threading.Thread(target=playsound, args=(audio_name,), daemon=True).start()
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

print(YouTube("https://www.youtube.com/watch?v=8UVNT4wvIGY").video_id)