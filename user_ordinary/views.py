from datetime import datetime, timedelta
import os, bcrypt, jwt

from django.conf import settings

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


from . import models


def match_nick(nickname):
    nick = models.UserOrdinary.objects.filter(nickname=nickname)
    return nick


def match_mail(mail):
    obj = models.UserOrdinary.objects.filter(mail=mail)
    return obj


# ...


def get_token(request):
    token = request.COOKIES.get("ordinary")

    if not token:
        raise PermissionDenied

    return token


def decode_token(request):
    token = get_token(request)

    if not token:
        pass

    payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    mail = payload["mail"]

    return mail


def get_user(request):

    mail = decode_token(request)

    if not mail:
        pass

    user = models.UserOrdinary.objects.get(mail=mail)
    return user


def get_active_user(request):

    user = get_user(request)

    if not user:
        messages.info(request, "ordinary active user to login..!")
        return redirect("ordinary/login")

    if not user.email_verified:
        messages.info(request, "reset email..!")
        return redirect("ordinary/reset-email")

    if not user.is_active:
        messages.info(request, "is active..!")
        return redirect("/")

    return user


def get_id(id):
    user = get_object_or_404(models.UserOrdinary, id=id)
    return user


def register(request):
    # ...
    if request.method == "GET":
        return render(request, "auth/ordinary/register.html")
    # ...
    if request.method == "POST":
        # ...
        nickname = request.POST.get("nickname")
        mail = request.POST.get("mail")
        pswd = request.POST.get("password")
        # ...
        res_nick = match_nick(nickname)
        res_mail = match_mail(mail)
        # ...
        if not res_nick:
            if not res_mail:
                # ...
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(pswd.encode(), salt)
                # ..

                models.UserOrdinary.objects.create(
                    nickname=nickname,
                    mail=mail,
                    password=hashed,
                    created_at=timezone.now(),
                )

                # ...
                payload = {
                    "mail": mail,
                    "exp": datetime.utcnow()
                    + timedelta(minutes=int(settings.EMAIL_TOKEN_EXPIRY_MINUTES)),
                    "iat": datetime.utcnow(),
                    "scope": "email_verification",
                }
                token = jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)
                # ...

                current_site = get_current_site(request)
                mail_subject = "activate your account"
                message = render_to_string(
                    "auth/ordinary/acc_active_email.html",
                    {
                        "user": mail,
                        "domain": current_site.domain,
                        "token": token,
                    },
                )
                to_email = mail
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.info(request, "open mail and follow the link")
                return redirect("/")
            messages.info(request, "such a email already exists")
            return redirect("/")
        messages.info(request, "such a nickname already exists")
        return redirect("/")


def login_view(request):
    # ...
    if request.method == "GET":
        return render(request, "auth/ordinary/login.html")
    # ...
    if request.method == "POST":
        mail = request.POST.get("mail")
        password = request.POST.get("password")
        # ...
        if match_mail(mail):
            # ...
            entry = models.UserOrdinary.objects.get(mail=mail)
            # ...
            if entry.email_verified:
                # ...
                if bcrypt.checkpw(password.encode(), entry.password):
                    # ...
                    payload = {
                        "id": entry.id,
                        "nickname": entry.nickname,
                        "mail": entry.mail,
                    }
                    ordinary = jwt.encode(
                        payload, settings.SECRET_KEY, settings.JWT_ALGORITHM
                    )

                    response = redirect("/")
                    response.set_cookie(
                        "ordinary",
                        ordinary,
                        path="/",
                        httponly=True,
                    )
                    return response

                messages.info(request, "Sorry.. The password doesn't match..!")
                return redirect("/")

            messages.info(request, "Sorry.. NO email verified..!")
            return redirect("/")

        messages.info(request, "Sorry.. NO email user..!")
        return redirect("/")


def mail_verify(request, token):
    # ...
    payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    mail = payload["mail"]
    # ...
    res = match_mail(mail)
    # ...
    entry = models.UserOrdinary.objects.get(mail=mail)
    # ...
    if not res:
        messages.info(request, "Invalid user..! Please create an account")
        return redirect("/")

    if entry.email_verified == 1:
        messages.info(request, "Email has already been verified!..")
        return redirect("/")

    entry.email_verified = 1
    entry.is_active = 1
    entry.save()

    messages.info(request, "your email address has been successfully confirmed..!")
    return redirect("/")


def reset_email(request):
    # ...
    if request.method == "GET":
        return render(request, "auth/resend_email.html")
    # ...
    if request.method == "POST":
        # ...
        mail = request.POST.get("mail")
        # ...
        user = match_mail(mail)
        # ...
        if not user:
            messages.info(request, "The user with this email address does not exist..!")
            return redirect("/")
        # ...
        entry = models.UserOrdinary.objects.get(mail=mail)
        # ...
        if entry.email_verified:
            messages.info(request, "email already verified..!")
            return redirect("/")

        # ...
        payload = {
            "mail": mail,
            "exp": datetime.utcnow()
            + timedelta(minutes=int(settings.EMAIL_TOKEN_EXPIRY_MINUTES)),
            "iat": datetime.utcnow(),
            "scope": "resend_verification_email",
        }
        token = jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        # ...

        current_site = get_current_site(request)
        mail_subject = "resend verification email"
        message = render_to_string(
            "auth/ordinary/acc_verification_email.html",
            {
                "user": mail,
                "domain": current_site.domain,
                "token": token,
            },
        )
        to_email = mail
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.info(request, "Confirmation email resent..!")
        return redirect("/")


def reset_verification_email(request, token):
    # ...
    payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    mail = payload["mail"]
    # ...
    res = match_mail(mail)
    # ...
    entry = models.UserOrdinary.objects.get(mail=mail)

    if not res:
        messages.info(request, "Invalid user..! Please create an account")
        return redirect("/")

    if entry.email_verified == 1:
        messages.info(request, "Email has already been verified!..")
        return redirect("/")

    entry.email_verified = 1
    entry.is_active = 1
    entry.modified_at = timezone.now()
    entry.save()

    messages.info(request, "your email address has been successfully confirmed..!")
    return redirect("/")


def reset_password(request):
    # ...
    if request.method == "GET":
        return render(request, "auth/reset_password.html")
    # ...
    if request.method == "POST":
        # ...
        mail = request.POST.get("mail")
        # ...
        user = match_mail(mail)
        # ...
        if not user:
            messages.info(request, "The user with this email address does not exist..!")
            return redirect("/")

        # ...
        payload = {
            "mail": mail,
            "exp": datetime.utcnow()
            + timedelta(minutes=int(settings.EMAIL_TOKEN_EXPIRY_MINUTES)),
            "iat": datetime.utcnow(),
            "scope": "reset_password",
        }
        token = jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        # ...

        current_site = get_current_site(request)
        mail_subject = "reset password"

        message = render_to_string(
            "auth/ordinary/acc_password_verification_email.html",
            {
                "user": mail,
                "domain": current_site.domain,
                "token": token,
            },
        )
        to_email = mail
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.info(request, "Confirmation email resent..!")
        return redirect("/")


def reset_password_confirm(request, token):
    # ...
    if request.method == "GET":
        # ...
        payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        mail = payload["mail"]
        # ...
        res = match_mail(mail)
        # ...
        if not res:
            messages.info(request, "Invalid user..! Please create an account")
            return redirect("/")
        return render(request, "auth/reset_password_confirm.html")
    # ...
    if request.method == "POST":
        # ...
        payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        mail = payload["mail"]
        # ...
        entry = models.UserOrdinary.objects.get(mail=mail)
        # ...
        password = request.POST.get("password")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        # ...
        entry.password = hashed
        entry.modified_at = timezone.now()
        entry.save()

        messages.info(request, "your email address has been successfully confirmed..!")
        return redirect("/")


# ...


def update_view(request, id):
    # ...
    if request.method == "GET":
        # ...
        if get_id(id) and get_active_user(request):
            # ...
            obj = get_id(id)
            user = get_user(request)
            # ...
            if obj.mail == user.mail:
                content = {"obj": obj}
                return render(request, "auth/ordinary/update.html", content)

            messages.info(request, "login..? not yours..")
            return redirect("/ordinary/login")
        return False
    # ...
    if request.method == "POST":
        # ...
        nickname = request.POST.get("nickname")
        file = request.FILES.get("file")
        # ...
        obj = get_id(id)
        # ...
        obj.nickname = nickname
        obj.file = file
        obj.save()

        messages.info(request, "OK..!")
        return redirect("/")
    messages.info(request, "Post ok..!")


def logout_view(request):
    # ...
    if request.method == "GET":
        # ...
        if get_active_user(request):
            return render(request, "auth/logout.html")
        return False
    # ...
    if request.method == "POST":
        # ...
        if get_active_user(request):
            # ...
            response = redirect("/")
            response.delete_cookie(key="ordinary", path="/")

            messages.info(request, "you have logged out of your account..!")
            return response
        return False


def delete_view(request, id):
    # ...
    if request.method == "GET":
        # ...
        if get_active_user(request):
            # ...
            return render(request, "auth/delete.html")
        return False
    # ...
    if request.method == "POST":
        # ...
        if get_active_user(request):
            # ...
            get_id(id).delete()
            # ...
            messages.info(request, "user delete..!")
            return redirect("/")

        return False
