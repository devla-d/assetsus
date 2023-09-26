from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    return render(request, "user/index.html")


@login_required()
def enable_2fa(request):
    return render(request, "user/2fa.html")
