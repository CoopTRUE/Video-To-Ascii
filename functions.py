from time import sleep, perf_counter
from PIL import Image
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS, CAP_PROP_POS_FRAMES, CAP_PROP_FRAME_COUNT
from pytube import YouTube
from youtube_search import YoutubeSearch
from typing import Optional, Sequence, Union
from moviepy.editor import VideoFileClip
from pygame import mixer
from pyfiglet import figlet_format
from os import get_terminal_size
from threading import Thread

def convert(
        image_data: Sequence[Sequence[Sequence[int]]],
        resize: Optional[Sequence[int]],
        ascii_chars: str,
        pixel_width: str,
    ) -> str:
    """Convert image data `image_data` into ASCII text with `ascii_chars` characters. Pixel width is `pixel_width`. See README.md for pixel width info. Optional 'resize' resizes the image. Returns the ASCII text as a `str`."""

    image_data = Image.fromarray(image_data)  # Create PIL Image object
    if resize:  # Optional resize
        image_data = image_data.resize(resize)
        width = resize[0]
    else:
        width = len(image_data[0])

    image_data = image_data.convert('L')  # Convert the image into shades of black
    image_data = image_data.getdata()  # Get the image data

    new_data = [
        ascii_chars[int(pixel_value/pixel_width)]
            for
        pixel_value
            in
        image_data
    ]
    length = len(new_data)
    split_data = [
        ''.join(new_data[index: index+width])
            for
        index
            in
        range(0, length, width)
    ]

    # The code above is too complicated to explain
    return '\n'.join(split_data)

def url_download(url: str) -> YouTube:
    """Download the youtube video with the url `url`. Returns the `YouTube` object."""
    yt = url_video(url)
    streams = yt.streams
    stream = streams.first()
    stream.download(filename='video')
    return yt

def get_custom_name(youtube_object: Union[YouTube, YoutubeSearch], show_title: bool = True) -> str:
    """Get custom folder name for dowling youtube videos. If `show_title` then print the video title as figlet text. Returns the custom name as a `str`."""
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
    """Return the `YouTube` object at url `url`."""
    return YouTube(url)

def search_video(video_name: str) -> YoutubeSearch:
    """Return the `YoutubeSearch` object searched with `video_name`."""
    return YoutubeSearch(video_name, max_results=1)

def search(video_name: str) -> dict:
    """Search youtube for the video `video_name`. Return the properties of the first video as a `dict`."""
    search = search_video(video_name)
    search_dict = search.to_dict()
    return search_dict[0]

def play_video(
        video: Union[str, VideoCapture],
        audio_name: str,
        width: Optional[int],
        height: Optional[int],
        ascii_chars: str,
        pixel_width: Union[int, float],
        buffer_delay: Union[float, int],
        frame_rate: Optional[Union[float, int]],
        threads: int
        # fast_forward = Optional[int]
    ) -> None:
    """Print each frame of video `video` at the frame rate of `frame_rate`.
    If `frame_rate` is not passed, the frame rate will default to video frame rate.
    Each frame is converted to ASCII with the character set of `ascii_chars` and the pixel_width `pixel_width`, printed at a constant frame rate with changing speed to accommodate conversion speed lag differences.
    The video will always be about `buffer_delay` faster than the audio but the buffer delay minimize `sleep` function slight incorrect time.
    Play the audio `audio_name`.
    Returns `None`."""

    # Set default arguments if not passed
    vidcap = video if isinstance(video, VideoCapture) else VideoCapture(video)
    WIDTH = width or vidcap.get(CAP_PROP_FRAME_WIDTH)
    HEIGHT = height or vidcap.get(CAP_PROP_FRAME_HEIGHT)
    FRAME_DELAY = 1/(frame_rate or vidcap.get(CAP_PROP_FPS))  # Frame rate should be 1/frame_rate
    TOTAL_FRAMES = vidcap.get(CAP_PROP_FRAME_COUNT)

    sleep(2)
    # THREAD MAGIC
    global image_frames
    image_frames = []
    ascii_frames = []

    global convert_index
    convert_index = -1

    def read_frame_thread():
        global image_frames
        success, raw_frame = vidcap.read()
        while success:
            image_frames.append(raw_frame)
            success, raw_frame = vidcap.read()

    def convert_thread(n):
        global convert_index
        while True:
            convert_index = convert_index + 1
            print("THREAD", n, "CONVERTING", convert_index)
            ascii_frame = convert(image_frames[convert_index], (WIDTH, HEIGHT), ascii_chars, pixel_width)
            ascii_frames.append(ascii_frame)

    read_threads = []
    for _ in range(threads):
        read_threads.append(Thread(target=read_frame_thread, args=(), daemon=True))
    for thread in read_threads:
        thread.start()
        sleep(0.3)

    convert_threads = []
    for i in range(threads):
        convert_threads.append(Thread(target=convert_thread, args=(i,), daemon=True))
    for thread in convert_threads:
        thread.start()


    sleep(1)


    # render_threads = []
    # converted_frames = []
    # def frames_thread():
    #     success, raw_frame = vidcap.read()
    #     image_frames.append(raw_frame)
    #     while success:
    #         success, raw_frame = vidcap.read()
    #         image_frames.append(raw_frame)
    # frame_reading_thread = Thread(target=frames_thread, daemon=True)
    # frame_reading_thread.start()

    # frame_render_index = -1
    # def ascii_render_thread(n):
    #     i = 0
    #     while True:
    #         i += n
    #         for thread_number in range(threads).__reversed__():
    #             if
    #         frame_to_render = image_frames[frame_reader_index]
    #         converted_frame = convert(frame_to_render, (WIDTH, HEIGHT), ascii_chars, pixel_width)
    #         converted_frames.append(converted_frame)
    #         # print("CONVERTED!")

    # def start_rendering_threads():
    #     for _ in range(threads):
    #         new_thread = Thread(target=ascii_render_thread, args=(), daemon=True)
    #         new_thread.start()
    #         render_threads.append(new_thread)
    #         sleep(0.1)
    # sleep(1)
    # main_rendering_thread = Thread(target=start_rendering_threads, args=(), daemon=True)
    # main_rendering_thread.start()
    # sleep(1)

    # Play music
    mixer.music.load(audio_name)
    # if fast_forward:
    #     print(fast_forward)
    #     vidcap.set(CAP_PROP_POS_FRAMES, fast_forward)
    # mixer.music.play(0, fast_forward / vidcap.get(CAP_PROP_FPS))
    mixer.music.play()
    buffer = 0
    current_frame = -1
    while True:
        old_time = perf_counter()
        current_frame += 1
        if current_frame == TOTAL_FRAMES:
            del read_thread
            del convert_threads
            break
        # print(chr(27))
        # print(ascii_frames[current_frame])
        if buffer_delay:  # If there should be a delay
        # Loop should wait `frame_rate` but the time it takes to convert should add onto that time
        # By having a buffer, the terminal can print as fast as it wants but once it gets faster than the buffer it will wait that buffer
            buffer = buffer + (FRAME_DELAY - (perf_counter() - old_time))
            if buffer >= buffer_delay:
                sleep(buffer_delay)
                buffer = buffer - buffer_delay  # Even though this may be an extremely small amount, little delays will completely de-sync audio
    # OLD NON-THREADED LOOP
    """while success:
        old_time = perf_counter()  # pref_counter is used for it's extreme accuracy
        text = convert(  # It converts the text lol what do you expect
            frame,
            (width, height),
            ascii_chars,
            pixel_width
        )
        print(chr(27))  # Very fast way of clearing the terminal
        print(text)
        success, frame = vidcap.read()  # Read next frame
        if buffer_delay:  # If there should be a delay
            # Loop should wait `frame_rate` but the time it takes to convert should add onto that time
            # By having a buffer, the terminal can print as fast as it wants but once it gets faster than the buffer it will wait that buffer
            buffer = buffer + (frame_rate - (perf_counter() - old_time))  #
            if buffer >= buffer_delay:
                sleep(buffer_delay)
                buffer = buffer - buffer_delay  # Even though this may be an extremely small amount, little delays will completely de-sync audio
    """
def make_audio(video_name: str, audio_name: str) -> None:
    """Make audio file with the file name of `audio_name` from the video `video_name`. Returns `None`."""
    with VideoFileClip(video_name) as video:
        video.audio.write_audiofile(audio_name)
