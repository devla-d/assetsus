from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.index, name="dashboard"),
    path("twofactor/", views.enable_2fa, name="enable_2fa"),
    path("disable-twofactor/", views.disable_2fa, name="disable_2fa"),
]
