from django.urls import path
from runtext import views

urlpatterns = [
    path('', views.index, name='index')
]