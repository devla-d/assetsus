from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from .models import Account
from .forms import LoginForm, RegisterForm
from django.contrib.auth.forms import SetPasswordForm
from baseapp import utils


def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            #  use cache to store the cleaned_data  till their email address has been verify and the code should last for  5min

            user_details = form.cleaned_data
            user_details["code"] = utils.gen_random_code(6)
            print(user_details)
            data = cache.get(user_details["email"])
            if data:
                cache.delete(user_details["email"])
            cache.set(user_details["email"], user_details, timeout=300)
            email_encode = urlsafe_base64_encode(force_bytes(user_details["email"]))

            subject = f"Verify your email address"
            context = {
                "user": user_details,
                "code": user_details.get("code"),
            }
            message = get_template("auth/verify.email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[user_details["email"]],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)

            messages.info(request, "Account creation submited please verify your email")

            return redirect("confirm_email", email=email_encode)

    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})


def confirm_email(request, email):
    is_encoding_correct = False
    email_decode = None

    try:
        email_decode = force_str(urlsafe_base64_decode(email))
        is_encoding_correct = True

    except:
        is_encoding_correct = False

    user_data = cache.get(email_decode)
    print(email_decode)
    if is_encoding_correct == False and email_decode is None:
        messages.info(request, "Link is invalid")
        return redirect("register")
    if user_data == None:
        messages.info(request, "Link is invalid")
        return redirect("register")

    if request.POST:
        input_code = request.POST.get("code")
        if input_code == user_data["code"]:
            cache.delete(email_decode)
            account = Account(
                email=user_data["email"],
                username=user_data["username"],
                country=user_data["country"],
                phone=f"{user_data['mobile_code']}{user_data['phone']}",
            )
            account.set_password(user_data["password1"])
            account.save()

            messages.info(request, "Account created you can now login")
            return redirect("login")
        else:
            messages.info(request, "Code is incorrect")
            return redirect("confirm_email", email=email)

    return render(request, "auth/confirm_mail.html")


def log_in(request):
    if request.user.is_authenticated:
        messages.warning(request, ("Already logged in"))
        return redirect("/dashboard")
    destination = utils.get_next_destination(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"], password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                if destination:
                    return redirect(f"{destination}")
                else:
                    return redirect("dashboard")
        # else:
        #     messages.warning(request, ("Invalid Email Or Password."))
        #     return redirect("login")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def authorizations(request):
    return render(request, "auth/authorization.html")


def reset_password(request):
    if request.POST:
        email = request.POST.get("email")
        accoun = None
        try:
            account = Account.objects.get(email__exact=email)
        except Account.DoesNotExist:
            account = None
        if account:
            data = cache.get(account.username)
            if data:
                cache.delete(account.username)
            cache.set(account.username, account, timeout=300)
            print(account)
            current_site = get_current_site(request)
            subject = "Reset Your Password"
            context = {
                "user": account,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(account.email)),
            }
            message = get_template("auth/resetpassword.email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[account.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)

            messages.success(
                request, (" check your mail box for instructions to continue")
            )
            return redirect("reset_password")

        else:
            messages.success(request, ("A User with this email does't exist"))
            return redirect("reset_password")
    return render(request, "auth/reset_password.html")


def new_password_view(
    request,
    uidb64,
):
    is_encoding_correct = False
    email = None

    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        is_encoding_correct = True

    except:
        is_encoding_correct = False

    account = utils.check_user(email, Account)
    user = cache.get(account.username)

    if is_encoding_correct == False and email is None:
        messages.info(request, "Link is invalid")
        return redirect("reset_password")
    if user == None:
        messages.info(request, "Link is invalid")
        return redirect("reset_password")

    if request.POST:
        form = SetPasswordForm(account, request.POST)

        if form.is_valid():
            form.save()
            cache.delete(account.username)
            messages.success(request, ("Your Password has been reset"))
            return redirect("login")

    else:
        form = SetPasswordForm(user=account)
    return render(request, "auth/new_password.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("login")
