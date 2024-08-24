from sys import argv

from moviepy.editor import CompositeVideoClip, TextClip


DEFAULT_DURATION = 3
DEFAULT_TEXT_COLOR = 'white'
DEFAULT_BG_COLOR = 'black'


def create_runtext_videofile(text: str, filename: str, *,
        duration: int = DEFAULT_DURATION, text_color: str = DEFAULT_TEXT_COLOR,
        bg_color: str = DEFAULT_BG_COLOR):
    """Create a running text video and save it as `filename`.
    
    mp4 doesn't support transparency btw."""

    if not isinstance(text, str) or len(text) == 0:
        raise ValueError('`text` must be a non-empty string.')
    if not isinstance(filename, str) or len(filename) == 0:
        raise TypeError('`filename` must be a non-empty string.')
    
    duration = DEFAULT_DURATION if duration is None else int(duration)
    text_color = DEFAULT_TEXT_COLOR if text_color is None else text_color
    bg_color = DEFAULT_BG_COLOR if bg_color is None else bg_color
    
    text = TextClip(text, color=text_color, bg_color=bg_color, size=(None, 100)) \
        .set_position(lambda t: (-t, 0))
    clip = CompositeVideoClip([text], (100, 100)) \
        .set_duration(text.size[0]) \
        .speedx(final_duration=duration)
    clip.write_videofile(filename, fps = 10, codec='libx264',
                         ffmpeg_params=['-f', 'mp4'])


if __name__ == '__main__':
    text = argv[1]
    try:
        file = argv[2]
    except IndexError:
        file = text + '.mp4'
    create_runtext_videofile(text, file)
