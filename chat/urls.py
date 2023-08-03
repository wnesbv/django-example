from django.urls import path

from . import views
from . import img


urlpatterns = [
    path("", views.index, name="ch_index"),
    path("<str:uustr>", views.room, name="room"),
]
