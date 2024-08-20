from sys import argv

from moviepy.editor import CompositeVideoClip, TextClip


def create_runtext_videofile(text: str, filename: str, /,
                     duration: int = 3, text_color: str = 'white',
                     bg_color: str = 'transparent'):
    """Create a running text video and save it as 'filename'.
    
    mp4 doesn't support transparency btw."""

    if not isinstance(text, str) or len(text) == 0:
        raise ValueError('`text` must be a non-empty string.')
    if not isinstance(filename, str) or len(filename) == 0:
        raise TypeError('`filename` must be a non-empty string.')
    
    text = TextClip(text, color=text_color, size=(None, 100)) \
        .set_position(lambda t: (-t, 0))
    clip = CompositeVideoClip([text], (100, 100)) \
        .set_duration(text.size[0]) \
        .speedx(final_duration=duration)
    clip.write_videofile(filename, fps = 10)


if __name__ == '__main__':
    text = argv[1]
    try:
        file = argv[2]
    except IndexError:
        file = text + '.mp4'
    create_runtext_videofile(text, file)
