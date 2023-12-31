
from django.urls import path

from core import views as core

from . import views, csv_export, csv_import


urlpatterns = [
    path(
        "register", views.register, name="privileged_register"
    ),

    path(
        "login/", views.login, name="privileged_login"
    ),
    path(
        "logout", views.logout_view, name="privileged_logout",
    ),
    # ...
    path(
        "activate/<token>/", views.mail_verify, name="privileged_activate"
    ),
    path(
        "reset-email", views.reset_email, name="privileged_resend_email",
    ),
    path(
        "reset-verification-email/<token>/",
        views.reset_verification_email,
        name="privileged_resend_verification_email",
    ),
    path(
        "reset-password", views.reset_password, name="privileged_resend_password",
    ),
    path(
        "reset-password-verification-email/<token>/",
        views.reset_password_confirm,
        name="privileged_resend_password_verification_email",
    ),
    # ...
    path(
        "details/<id>/", core.details_privileged, name="details_privileged"
    ),
    path(
        "update/<id>/", views.update_view, name="privileged_update"
    ),
    path(
        "delete/<id>/", views.delete_view, name="privileged_delete"
    ),
    # ..
    path(
        "import-csv/", csv_import.import_csv, name="ordinary_import_csv"
    ),
    path(
        "export-csv/", csv_export.export_csv, name="ordinary_export_csv"
    ),

]
