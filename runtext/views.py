from tempfile import NamedTemporaryFile
from urllib.parse import urlencode

from django.conf import settings
from django.http import FileResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from .models import Generation, Request

from . import runtext_engine as engine
from .runtext_engine import create_runtext_videofile


def serve_demo(request):
    Request.objects.create(request_type=Request.DEMO)
    url = '{}?{}'.format(
        reverse('create'),
        urlencode(dict(
                video_text='This is a demo runing text video',
                duration=engine.DEFAULT_DURATION,
                text_color=engine.DEFAULT_TEXT_COLOR,
                bg_color=engine.DEFAULT_BG_COLOR
            )
        )
    )
    return redirect(url)


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
