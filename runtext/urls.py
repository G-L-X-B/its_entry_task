from django.urls import path
from . import views

urlpatterns = [
    path('<str:video_text>', views.generate_video),
    path('demo', views.serve_demo, name='demo'),
]
