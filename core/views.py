
import os
from datetime import datetime, timedelta
from pathlib import Path, PurePosixPath

from PIL import Image

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from user_privileged import models as pri_models, views as pri_views
from user_ordinary import models as ord_models, views as ord_views


def Index_view(request):

    template = "auth/privileged/privileged.html"

    if request.COOKIES.get("privileged"):
        session_key = request.COOKIES.get("sessionid")
        session = Session.objects.get(session_key=session_key)

        obj = session.get_decoded()

        # uid = session.get_decoded().get('_auth_user_id')
        # user = User.objects.get(pk=uid)
        # print(user.username, user.get_full_name(), user.email)

        privileged_list = pri_models.UserPrivileged.objects.all()
        privileged = pri_views.get_active_user(request)
        privileged_owning = pri_views.match_mail(privileged)
        # ...
        ordinary_list = ord_models.UserOrdinary.objects.all()

        content = {
            "obj": obj,
            "privileged_list": privileged_list,
            "privileged": privileged,
            "privileged_owning": privileged_owning,
            "ordinary_list": ordinary_list,
        }

        return render(request, template, content)

    if request.COOKIES.get("ordinary"):
        # ...
        privileged_list = pri_models.UserPrivileged.objects.all()
        # ...
        ordinary_list = ord_models.UserOrdinary.objects.all()
        ordinary = ord_views.get_active_user(request)
        ordinary_owning = ord_views.match_mail(ordinary)

        content = {
            "privileged_list": privileged_list,
            "ordinary_list": ordinary_list,
            "ordinary": ordinary,
            "ordinary_owning": ordinary_owning,
        }

        return render(request, "auth/ordinary/ordinary.html", content)

    privileged_list = pri_models.UserPrivileged.objects.all()
    ordinary_list = ord_models.UserOrdinary.objects.all()

    content = {
        "privileged_list": privileged_list,
        "ordinary_list": ordinary_list,
    }

    return render(request, "index.html", content)


def details_ordinary(request, id):
    i = ord_models.UserOrdinary.objects.get(id=id)

    content = {
        "i": i,
    }
    return render(request, "auth/ordinary/details.html", content)


def details_privileged(request, id):
    i = pri_models.UserPrivileged.objects.get(id=id)

    content = {
        "i": i,
    }
    return render(request, "auth/privileged/details.html", content)
