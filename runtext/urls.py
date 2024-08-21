from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_video, name='create'),
    path('demo', views.serve_demo, name='server_demo'),
]
