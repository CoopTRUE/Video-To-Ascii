# Video-To-Ascii
Video-To-Ascii is a video player and YouTube downloader converted into ascii in realtime and printed in the terminal

## Requirements
- Python3
- Cv2
- Pillow
- Moviepy
- Pygame (Used for audio)
- youtube-dl (for some reason Pytube download is broken)
- Pytube
- Youtube_search
- Windows ...for now



## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the needed packages.
```bash
pip install -r requirements.txt
```

## How to use
Just run `main.py`

## Features
- Fully working YouTube video downloader from search or url
- Video download organization in folders easily deletable
- Mp3 audio extraction from video and player
- FULLY SYNCED FRAME TIMES. Using buffering and some smart python trickery, the frames will always be in sync with the audio
- Customizable ascii characters and settings
- Last video played remembering for easy video playback

## Snippets

Type hint galore
```python
def raw_play_video(
        video: Union[str, VideoCapture],
        audio_name: str,
        width: Optional[int],
        height: Optional[int],
        ascii_chars: str,
        pixel_width: Union[int, float],
        buffer_delay: Union[float, int],
        frame_rate: Optional[Union[float, int]] = None,
    ) -> None:
```

Extreme logic
```python
    selected_video = settings['lastVideo'] = (
        last_video if forced_load else forced_load
        or input("\n\n\nFILENAME, FOLDER NAME, YOUTUBE URL, OR YOUTUBE SEARCH: ")
        or last_video
    )
```

BUILT FOR WINDOWS 10 PYTHON 3.9.5