from django.db import models

from .runtext_engine import DEFAULT_BG_COLOR, DEFAULT_DURATION, DEFAULT_TEXT_COLOR


class Generation(models.Model):
    text = models.TextField()
    duration = models.IntegerField(default=DEFAULT_DURATION)
    text_color = models.TextField(default=DEFAULT_TEXT_COLOR)
    bg_color = models.TextField(DEFAULT_BG_COLOR)


class Request(models.Model):
    DEMO = 'demo'
    CREATE = 'create'
    REQUEST_TYPE_CHOICES = {
        DEMO: 'Show Demo',
        CREATE: 'Create Video'
    }
    request_type = models.CharField(max_length=32, choices=REQUEST_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    generation_options = models.ForeignKey(Generation, null=True, default=None,
                                           on_delete=models.CASCADE)
