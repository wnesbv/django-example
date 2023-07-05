
from django.urls import path

from core import views as core

from . import views, csv_export, csv_import


urlpatterns = [
    path(
        "register", views.register, name="ordinary_register"
    ),
    path(
        "login", views.login_view, name="ordinary_login"
    ),
    path(
        "logout", views.logout_view, name="ordinary_logout",
    ),
    # ...
    path(
        "activate/<token>/", views.mail_verify, name="ordinary_activate"
    ),
    path(
        "reset-email", views.reset_email, name="ordinary_resend_email",
    ),
    path(
        "reset-verification-email/<token>/",
        views.reset_verification_email,
        name="ordinary_resend_verification_email",
    ),
    path(
        "reset-password", views.reset_password, name="ordinary_resend_password",
    ),
    path(
        "reset-password-verification-email/<token>/",
        views.reset_password_confirm,
        name="ordinary_resend_password_verification_email",
    ),
    # ...
    path(
        "details/<id>/", core.details_ordinary, name="details_ordinary"
    ),
    path(
        "update/<id>/", views.update_view, name="ordinary_update"
    ),
    path(
        "delete/<id>/", views.delete_view, name="ordinary_delete"
    ),
    # ..
    path(
        "import-csv/", csv_import.import_csv, name="ordinary_import_csv"
    ),
    path(
        "export-csv/", csv_export.export_csv, name="ordinary_export_csv"
    ),

]
