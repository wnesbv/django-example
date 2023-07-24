from datetime import datetime
from pathlib import Path

import tempfile, bcrypt, csv, uuid

from django.shortcuts import render, redirect
from django.contrib import messages

from . import views, models


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
root_directory = BASE_DIR / "static/upload"


def result_csv_ordinary(request):
    user = views.get_active_user(request)
    result = models.UserOrdinary.objects.get(mail=user.mail)
    return result


def import_csv(request):
    template = "auth/ordinary/import_csv.html"

    if request.method == "GET":
        context = {"request": request}
        return render(request, template, context)

    # ...
    if request.method == "POST":
        # ..
        url_f = request.FILES.get("url_f")
        # ..
        temp = tempfile.NamedTemporaryFile(delete=False)
        print("temp name..", temp.name)

        contents = url_f.file.read()

        with temp as csvf:
            csvf.write(contents)

        url_f.file.close()
        salt = bcrypt.gensalt()

        with open(temp.name, "r", encoding="utf-8") as csvfile:
            models.UserOrdinary.objects.bulk_create(
                [
                    models.UserOrdinary(
                        **{
                            "nickname": i["nickname"],
                            "mail": i["mail"],
                            # "password": bytes(i["password"], encoding='utf8'),
                            "password": bcrypt.hashpw(("password").encode(), salt),
                            "file": i["file"],
                            "identifier": uuid.uuid4().hex,
                            "is_active": i["is_active"],
                            "email_verified": i["email_verified"],
                            "created_at": datetime.now(),
                        }
                    )
                    for i in csv.DictReader(csvfile)
                ]
            )

            csvfile.close()
            Path.unlink(f"{temp.name}")

            return redirect("/")


# ...
# def import_csv(request):
#     template = "auth/ordinary/import_csv.html"

#     if request.method == "GET":
#         if views.get_active_user(request):
#             # ..
#             context = {"request": request}
#             return render(request, template, context)
#         messages.info(request, "You are banned - this is not your account..!")
#         return redirect("/")

#     # ...
#     if request.method == "POST":
#         # ..
#         url_f = request.FILES.get("url_f")
#         # ..
#         temp = tempfile.NamedTemporaryFile(delete=False)
#         print("temp name..", temp.name)

#         contents = url_f.file.read()

#         with temp as csvf:
#             csvf.write(contents)

#         url_f.file.close()

#         with open(temp.name, "r", encoding="utf-8") as csvfile:
#             models.UserOrdinary.objects.bulk_create(
#                 [
#                     models.UserOrdinary(
#                         **{
#                             "nickname": i["nickname"],
#                             "mail": i["mail"],
#                             "password": bytes(i["password"], encoding='utf8'),
#                             "file": i["file"],
#                             "identifier": uuid.uuid4().hex,
#                             "is_active": i["is_active"],
#                             "email_verified": i["email_verified"],
#                             "created_at": datetime.now(),
#                         }
#                     )
#                     for i in csv.DictReader(csvfile)
#                 ]
#             )

#             csvfile.close()
#             Path.unlink(f"{temp.name}")

#             return redirect("/")
