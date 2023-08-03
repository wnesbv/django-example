
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="ch_index"),
    path("<str:uustr>", views.room, name="room"),
]
