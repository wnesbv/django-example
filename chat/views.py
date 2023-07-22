
from django.shortcuts import render

from user_ordinary.models import UserOrdinary
from user_privileged.models import UserPrivileged

from user_privileged.views import privileged_user
from user_ordinary.views import token_user
from . import models


def index(request):

    or_list = UserOrdinary.objects.all()
    pr_list = UserPrivileged.objects.all()
    content = {
        "or_list": or_list,
        "pr_list": pr_list,
    }
    return render(request, "chat/index.html", content)


def room(request, uustr):

    if "privileged" in request.COOKIES:
        privileged = privileged_user(request)
        pr_list = models.UserChat.objects.filter(recipient=uustr, pr_chat=privileged)
        content = {
            "uustr": uustr,
            "pr_list": pr_list,
        }
        return render(request, "chat/room.html", content)
    if "ordinary" in request.COOKIES:
        or_list = models.UserChat.objects.filter(recipient=uustr, or_chat=privileged)

        content = {
            "uustr": uustr,
            "or_list": or_list,
        }
        return render(request, "chat/room.html", content)
