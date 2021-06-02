from time import sleep, perf_counter
from PIL import Image
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from pytube import YouTube
from youtube_search import YoutubeSearch
from typing import Optional, Sequence, Union
from moviepy.editor import VideoFileClip
from pygame import mixer
from pyfiglet import figlet_format
from os import get_terminal_size, getcwd, chdir, startfile
from shutil import rmtree

# ASCII_CHARS = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
ASCII_CHARS = ' .\'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
PIXEL_WIDTH = round(255 / (len(ASCII_CHARS)-1), 2)
PRIORITIZE = 'max'  # 'ratio' or 'max'
BUFFER_DELAY = .03  # Default 0.06.  0.03 for 8
SIDE_BY_SIDE_COMPARISON = False



mixer.init()
def convert_data(image_data: Sequence[Sequence[Sequence[int]]], ascii_chars, pixel_width, resize: Optional[Sequence[int]] = None) -> str:
    """Convert image data into ASCII text and optional resizes the image. Returns the ASCII text"""
    image_data = Image.fromarray(image_data)
    if resize:
        image_data = image_data.resize((resize))
        WIDTH = resize[0]
    else:
        WIDTH = len(image_data[0])
    image_data = image_data.convert('L')

    image_data = image_data.getdata()

    new_data = [ascii_chars[int(pixel_value/pixel_width)] for pixel_value in image_data]
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

def get_custom_name(youtube_object: Union[YouTube, YoutubeSearch], show_title: bool = True) -> str:
    if isinstance(youtube_object, YouTube):
        id = youtube_object.video_id
        title = youtube_object.title
    elif isinstance(youtube_object, YoutubeSearch):
        video_dict = youtube_object.to_dict()[0]
        id = video_dict['id']
        title = video_dict['title']
    else:
        raise TypeError
    if show_title: print(figlet_format(title, font='doh', width=get_terminal_size().columns))
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

def play_video(name: str, height: int, write_audio: bool = True, frame_rate: Optional[Union[float, int]] = None):
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