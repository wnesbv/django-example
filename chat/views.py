
from django.shortcuts import render

from user_ordinary.models import UserOrdinary
from user_privileged.models import UserPrivileged

from user_ordinary.views import get_active_user

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

    if request.method == "GET":

        if "sessionid" in request.COOKIES:

            admin_list = models.UserChat.objects.prefetch_related(
                "user_chat", "pr_chat", "or_chat"
            ).filter(recipient=uustr)
            content = {
                "uustr": uustr,
                "admin_list": admin_list,
            }
            return render(request, "chat/room.html", content)


        if "privileged" in request.COOKIES:

            pr_list = models.UserChat.objects.prefetch_related(
                "user_chat", "pr_chat", "or_chat"
            ).filter(recipient=uustr)
            content = {
                "uustr": uustr,
                "pr_list": pr_list,
            }
            return render(request, "chat/room.html", content)


        if "ordinary" in request.COOKIES:

            ordinary = get_active_user(request)

            or_list = models.UserChat.objects.prefetch_related(
                "user_chat", "pr_chat", "or_chat"
            ).filter(recipient=uustr)
            content = {
                "uustr": uustr,
                "or_list": or_list,
                "ordinary": ordinary,
            }
            return render(request, "chat/room.html", content)


    return render(request, "chat/room.html", {"uustr": uustr,})
