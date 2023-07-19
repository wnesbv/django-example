
from django.shortcuts import render

from user_ordinary.models import UserOrdinary
from user_privileged.models import UserPrivileged

from . import models


def index(request):

    or_list = UserOrdinary.objects.all()
    pr_list = UserPrivileged.objects.all()

    content = {
        "or_list": or_list,
        "pr_list": pr_list,
    }

    return render(request, "chat/index.html", content)


def room(request, user_id):

    models.UserChat.objects.filter(recipient=user_id)

    return render(request, "chat/room.html", {"user_id": user_id})
