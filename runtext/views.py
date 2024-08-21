from django.http import FileResponse
# from django.shortcuts import render
from django.conf import settings


def index(request):
    return FileResponse(
        open(settings.BASE_DIR / 'Hello, brotha!.mp4', 'rb'),
        as_attachment=True,
        filename='Hello, brotha!.mp4'
    )
