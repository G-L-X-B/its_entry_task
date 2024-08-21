from tempfile import NamedTemporaryFile

from django.http import FileResponse, HttpRequest
# from django.shortcuts import render
from django.conf import settings

from .runtext_engine import create_runtext_videofile


def serve_demo(request):
    return FileResponse(
        open(settings.BASE_DIR / 'Hello, brotha!.mp4', 'rb'),
        as_attachment=True,
        filename='Hello, brotha!.mp4'
    )


def generate_video(request: HttpRequest):
    video_text = request.GET['video_text']
    tmpfile = NamedTemporaryFile(buffering=0)
    create_runtext_videofile(video_text, tmpfile.name)
    return FileResponse(
        tmpfile,
        as_attachment=True,
        filename=video_text + '.mp4'
    )
