from django.urls import path, include
from . import views

urlpatterns = [
    path('chatbox/', views.chatbox, name='chatbox'),
]
