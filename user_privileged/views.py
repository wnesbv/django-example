
from datetime import datetime, timedelta
import os, jwt

from passlib.hash import pbkdf2_sha256

from django.conf import settings

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login as privileged_loginv

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from . import models


def match_username(username):
    username = User.objects.filter(username=username)
    return username


def match_mail(mail):
    mail = models.UserPrivileged.objects.filter(mail=mail)
    return mail


# ...


def get_token(request):
    token = request.COOKIES.get("privileged")
    return token

def decode_token(request):

    while True:
        token = get_token(request)
        if not token:
            break
        payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        mail = payload["mail"]

        return mail


def get_user(request):

    while True:
        mail = decode_token(request)

        if not mail:
            break

        user = models.UserPrivileged.objects.get(mail=mail)

        if not user:
            messages.info(request, "register..!")
            return redirect("privileged/register")
        return user


def get_active_user(request):

    user = get_user(request)

    if not user:
        messages.info(request, "login..!")
        return redirect("privileged/login")

    if not user.email_verified:
        messages.info(request, "reset email..!")
        return redirect("privileged/reset-email")

    if not user.is_active:
        messages.info(request, "is active..!")
        return redirect("/")

    return user


def get_id(id):

    user = get_object_or_404(models.UserPrivileged, id=id)
    return user


def register(request):
    # ...
    if request.method == "GET":
        return render(request, "auth/privileged/register.html")
    # ...
    if request.method == "POST":
        # ...
        username = request.POST.get("username")
        mail = request.POST.get("mail")
        pswd = request.POST.get("password")
        # ...
        res_nick = match_username(username)
        res_mail = match_mail(mail)

        if not res_nick:
            if not res_mail:
                hashed = pbkdf2_sha256.hash(pswd)
                # ..

                models.UserPrivileged.objects.create(
                    username=username,
                    mail=mail,
                    password=hashed,
                    is_active=False,
                    created_at=timezone.now(),
                )

                # ..
                payload = {
                    "mail": mail,
                    "exp": datetime.utcnow()
                    + timedelta(minutes=int(settings.EMAIL_TOKEN_EXPIRY_MINUTES)),
                    "iat": datetime.utcnow(),
                    "scope": "email_verification",
                }
                token = jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)
                # ..

                current_site = get_current_site(request)
                mail_subject = "activate your account"
                message = render_to_string(
                    "auth/privileged/acc_active_email.html",
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
        messages.info(request, "such a username already exists")
        return redirect("/")


def login(request):
    # ...
    if request.method == "GET":
        return render(request, "auth/privileged/login.html")
    # ...
    if request.method == "POST":
        # ...
        username = request.POST.get("username")
        password = request.POST.get("password")
        mail = request.POST.get("mail")
        # ...
        entry = models.UserPrivileged.objects.get(mail=mail)
        # ...
        if entry.email_verified:
            # ...
            if match_username(username):
                # ...
                user = models.User.objects.get(username=username)
                # ...
                if pbkdf2_sha256.verify(password, user.password):
                    # ...
                    privileged_loginv(request, user)
                    # ...
                    payload = {
                        "id": user.id,
                        "username": user.username,
                        "mail": entry.mail,
                    }

                    privileged = jwt.encode(
                        payload, settings.SECRET_KEY, settings.JWT_ALGORITHM
                    )
                    # ...

                    response = redirect("/")
                    response.set_cookie(
                        "privileged",
                        privileged,
                        path="/",
                        httponly=True,
                    )
                    return response

                messages.info(request, "Sorry.. The password doesn't match..!")
                return redirect("/")

            messages.info(request, "Sorry.. NO user..!")
            return redirect("/")

        messages.info(request, "Sorry.. NO email verified..!")
        return redirect("/")


def mail_verify(request, token):
    # ...
    payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    mail = payload["mail"]
    # ...
    res = match_mail(mail)
    # ...
    entry = models.UserPrivileged.objects.get(mail=mail)

    if not res:
        messages.info(request, "Invalid user..! Please create an account")
        return redirect("/")

    if entry.email_verified == 1:
        # ...
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

        if not user:
            messages.info(request, "The user with this email address does not exist..!")
            return redirect("/")
        # ...
        entry = models.UserPrivileged.objects.get(mail=mail)
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
            "auth/privileged/acc_verification_email.html",
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
    entry = models.UserPrivileged.objects.get(mail=mail)
    # ...
    if not res:
        messages.info(request, "Invalid user..! Please create an account")
        return redirect("/")
    # ...
    if entry.email_verified == 1:
        # ...
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
        token = jwt.encode(
            payload, settings.SECRET_KEY, settings.JWT_ALGORITHM
        )
        # ...

        current_site = get_current_site(request)
        mail_subject = "reset password"
        message = render_to_string(
            "auth/privileged/acc_password_verification_email.html",
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
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.JWT_ALGORITHM
        )
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
        entry = models.UserPrivileged.objects.get(mail=mail)

        password = request.POST.get("password")
        hashed = pbkdf2_sha256.hash(password)

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
            # ...
            content = {"obj": obj}
            return render(request, "auth/privileged/update.html", content)

        messages.info(request, "login..")
        return redirect("privileged/login")
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


def logout_view(request):
    # ...
    if request.method == "GET":
        # ...
        if get_active_user(request):
            return render(request, "auth/logout.html")
    # ...
    if request.method == "POST":
        # ...
        if request.user:
            # ...
            logout(request)
            # ...
            response = redirect("/")
            response.delete_cookie(key="privileged", path="/")

            messages.info(request, "you have logged out of your account..!")
            return response


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
