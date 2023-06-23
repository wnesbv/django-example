
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.conf import settings

from user_privileged import models as pri_models, views as pri_views
from user_ordinary import  models as ord_models, views as ord_views


def Index_view(request):

    if request.COOKIES.get("ordinary") and request.COOKIES.get("privileged"):

        privileged_list = pri_models.UserPrivileged.objects.all()
        privileged = pri_views.get_active_user(request)
        privileged_owning = pri_views.match_mail(privileged)
        # ...
        ordinary_list = ord_models.UserOrdinary.objects.all()
        ordinary = ord_views.get_active_user(request)
        ordinary_owning = ord_views.match_mail(ordinary)

        content = {
            "privileged_list": privileged_list,
            "privileged": privileged,
            "privileged_owning": privileged_owning,
            "ordinary_list": ordinary_list,
            "ordinary": ordinary,
            "ordinary_owning": ordinary_owning,
        }

        return render(request, "index.html", content)

    privileged_list = pri_models.UserPrivileged.objects.all()
    # ...
    ordinary_list = ord_models.UserOrdinary.objects.all()

    content = {
        "privileged_list": privileged_list,
        "ordinary_list": ordinary_list,
    }

    return render(request, "all_user.html", content)
