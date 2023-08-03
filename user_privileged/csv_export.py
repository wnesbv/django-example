
from datetime import datetime

import csv

from django.http import HttpResponse

from . import views, models


# ...
def export_csv(request):
    if request.method == "GET":

        if views.get_active_user(request):

            f_time = datetime.now()
            response = HttpResponse()
            response[
                "Content-Disposition"
            ] = f"attachment;filename=pr_{f_time.strftime('%Y-%m-%d-%H-%M-%S')}.csv"

            result = models.UserPrivileged.objects.all()
            writer = csv.writer(response)
            writer.writerow(
                [
                    "id",
                    "username",
                    "password",
                    "is_active",
                    "nickname",
                    "mail",
                    "file",
                    "identifier",
                    "email_verified",
                    "created_at",
                    "modified_at",
                    "user_ptr_id",
                ]
            )
            for i in result:
                writer.writerow(
                    [
                        i.id,
                        i.username,
                        i.password,
                        i.is_active,
                        i.nickname,
                        i.mail,
                        i.file,
                        i.identifier,
                        i.email_verified,
                        i.created_at,
                        i.modified_at,
                        i.user_ptr_id,
                    ]
                )

            return response
        return False
