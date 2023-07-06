from datetime import datetime
from pathlib import Path

import tempfile, csv

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from . import views, models


from import_export import resources


class PersonResource(resources.ModelResource):
    class Meta:
        model = models.UserPrivileged


from tablib import Dataset


def import_csv(request):
    if request.method == "POST":
        resource = PersonResource()
        dataset = Dataset()
        csvfile = request.FILES["url_f"]

        imported_data  = dataset.load(csvfile.read().decode('utf-8'), format="csv")
        print(" imported_data..", imported_data )

        result = resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            resource.import_data(dataset, dry_run=False)


    template = "auth/privileged/import_csv.html"
    return render(request, template)


# def import_csv(request):
#     template = "auth/privileged/import_csv.html"

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

#             models.UserPrivileged.objects.bulk_create(
#                 [
#                     models.UserPrivileged(
#                         **{
#                             "username": i["username"],
#                             "password": i["password"],
#                             "is_active": i["is_active"],
#                             "nickname": i["nickname"],
#                             "mail": i["mail"],
#                             "file": i["file"],
#                             "email_verified": i["email_verified"],
#                             "created_at": datetime.now(),
#                             "user_ptr_id": i["user_ptr"],
#                         }
#                     )
#                     for i in csv.DictReader(csvfile)
#                 ]
#             )

#             csvfile.close()
#             Path.unlink(f"{temp.name}")

#             return redirect("/")
