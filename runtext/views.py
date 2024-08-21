from tempfile import NamedTemporaryFile

from django.conf import settings
from django.http import FileResponse, HttpRequest
# from django.shortcuts import render


from .models import Generation, Request

from .runtext_engine import create_runtext_videofile


def serve_demo(request):
    Request.objects.create(request_type=Request.DEMO)
    return FileResponse(
        open(settings.BASE_DIR / 'Hello, brotha!.mp4', 'rb'),
        as_attachment=True,
        filename='Hello, brotha!.mp4'
    )


def create_video(request: HttpRequest):
    video_text = request.GET['video_text']
    opts = {
        option: request.GET[option]
        for option in ('duration', 'text_color', 'bg_color')
        if request.GET.get(option) is not None
    }
    gen = Generation.objects.create(text=video_text, **opts)
    Request.objects.create(request_type=Request.CREATE, generation_options=gen)
    tmpfile = NamedTemporaryFile(buffering=0)
    create_runtext_videofile(video_text, tmpfile.name, **opts)
    return FileResponse(
        tmpfile,
        as_attachment=True,
        filename=video_text + '.mp4'
    )
