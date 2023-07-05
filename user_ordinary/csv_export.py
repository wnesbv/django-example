
from datetime import datetime

import csv

from django.http import HttpResponse

from . import views, models


def result_csv_ordinary(request):
    user = views.get_active_user(request)
    result = models.UserOrdinary.objects.get(mail=user.mail)
    return result


# ...
def export_csv(request):
    if request.method == "GET":

        if views.get_active_user(request):

            f_time = datetime.now()
            response = HttpResponse()
            response[
                "Content-Disposition"
            ] = f"attachment;filename=or_{f_time.strftime('%Y-%m-%d-%H-%M-%S')}.csv"

            result = models.UserOrdinary.objects.all()
            writer = csv.writer(response)
            writer.writerow(
                [
                    "id",
                    "nickname",
                    "mail",
                    "password",
                    "file",
                    "is_active",
                    "email_verified",
                    "created_at",
                    "modified_at",
                ]
            )
            for i in result:
                writer.writerow(
                    [
                        i.id,
                        i.nickname,
                        i.mail,
                        (i.password).decode(),
                        i.file,
                        i.is_active,
                        i.email_verified,
                        i.created_at,
                        i.modified_at,
                    ]
                )

            return response
        return False
    return False
