
import os
from datetime import datetime, timedelta
from pathlib import Path, PurePosixPath

from PIL import Image

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from . import views


def img_creat(
    request, file, mdl
):

    dtm = datetime.now()
    year = dtm.strftime("%Y")
    month = dtm.strftime("%m")
    day = dtm.strftime("%d")

    user = views.get_user(request)
    save_path = f"./static/upload/{mdl}/{user}/{year}/{month}/{day}/"
    file_path = f"{save_path}/{file.name}"

    ext = PurePosixPath(file.name).suffix
    if ext not in (".png", ".jpg", ".jpeg"):
        messages.info(request, "Format files: png, jpg, jpeg ..!")

    if Path(file_path).exists():
        messages.info(request, "Error..! File exists..!")

    os.makedirs(save_path, exist_ok=True)

    with open(f"{file_path}", "wb") as fle:
        fle.write(file.file.read())

    return file_path.replace(".", "", 1)


def img_url(
    request, file, mdl
):

    dtm = datetime.now()
    year = dtm.strftime("%Y")
    month = dtm.strftime("%m")
    day = dtm.strftime("%d")

    user = views.get_user(request)
    save_path = f"./static/upload/{mdl}/{user}/{year}/{month}/{day}/"
    file_path = f"{save_path}/{file.name}"

    return file_path


def img_size(
    request, file, mdl, basewidth
):
    url = img_url(request, file, mdl)
    img = Image.open(f"{url}")
    # ..
    wpercent = basewidth/float(img.size[0])
    hsize = int((float(img.size[1])*float(wpercent)))
    # ..
    img_resize = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    img_resize.save(f"{url}")

    return img_resize
