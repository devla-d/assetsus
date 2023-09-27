from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from baseapp import utils
from django.contrib import messages

import pyotp


@login_required()
def index(request):
    return render(request, "user/index.html")


@login_required()
def enable_2fa(request):
    user = request.user

    otp_secret_key = utils.generate_totp_secret()

    qr_code = utils.generate_qr_code(otp_secret_key, user)

    if request.POST:
        secret_key = request.POST.get("key")
        code = request.POST.get("code")

        totp = pyotp.TOTP(secret_key)

        if totp.verify(code):
            user.otp_secret_key = secret_key
            user.otp_enabled = True
            user.save()
            messages.info(request, "2FA has been activated")
            return redirect("enable_2fa")
        else:
            messages.info(request, "Code in invalid")
            return render(
                request,
                "user/2fa.html",
                {"qr_code": qr_code, "otp_secret_key": secret_key},
            )

    return render(
        request, "user/2fa.html", {"qr_code": qr_code, "otp_secret_key": otp_secret_key}
    )


@login_required()
def disable_2fa(request):
    user = request.user
    if request.POST:
        code = request.POST.get("code")
        totp = pyotp.TOTP(user.otp_secret_key)
        if totp.verify(code):
            user.otp_secret_key = ""
            user.otp_enabled = False
            user.save()
            messages.info(request, "2FA has been deactivated")
            return redirect("enable_2fa")
        else:
            messages.info(request, "code is invalid")
            return redirect("enable_2fa")
    messages.info(request, "SOMETHING WENT WRONG")
    return redirect("enable_2fa")
