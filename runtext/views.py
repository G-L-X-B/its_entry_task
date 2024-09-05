from tempfile import NamedTemporaryFile
from urllib.parse import urlencode

from django.conf import settings
from django.http import FileResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Generation, Request

from . import runtext_engine as engine
from .runtext_engine import create_runtext_videofile


def _create_default_link(request):
    return '{}?{}'.format(
        request.build_absolute_uri(reverse('create')),
        urlencode(dict(
                video_text='This is a demo runing text video',
                duration=engine.DEFAULT_DURATION,
                text_color=engine.DEFAULT_TEXT_COLOR,
                bg_color=engine.DEFAULT_BG_COLOR,
            )
        )
    )


def serve_demo(request):
    Request.objects.create(request_type=Request.DEMO)
    return redirect(_create_default_link(request))


def create_video(request: HttpRequest):
    video_text = request.GET.get('video_text')
    if video_text is None:
        return redirect(help_page)
    opts = {
        option: request.GET[option]
        for option in ('duration', 'text_color', 'bg_color')
        if request.GET.get(option) is not None
    }
    if _check_creation_options(opts) is not None:
        return redirect(help_page)
    gen = Generation.objects.create(text=video_text, **opts)
    Request.objects.create(request_type=Request.CREATE, generation_options=gen)
    tmpfile = NamedTemporaryFile(buffering=0)
    try:
        create_runtext_videofile(video_text, tmpfile.name, **opts)
    except Exception as e:
        print(f'Error creating video: {e} (request id: {gen.id}).')
        return redirect(help_page)
    return FileResponse(
        tmpfile,
        as_attachment=True,
        filename=video_text + '.mp4'
    )


def _check_creation_options(options: dict):
    duration = options.get('duration')
    if duration is not None and int(duration) < 1:
        return 'duration'
    return None


def help_page(request: HttpRequest):
    return render(request, 'runtext/help.html', {
                    'create': request.build_absolute_uri(reverse('create')),
                    'default_duration': engine.DEFAULT_DURATION,
                    'default_text_color': engine.DEFAULT_TEXT_COLOR,
                    'default_bg_color': engine.DEFAULT_BG_COLOR,
                    'demo_link': request.build_absolute_uri(reverse('demo')),
                    'create_demo_link': _create_default_link(request),
                  })
