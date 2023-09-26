from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.log_in, name="login"),
    path("register/", views.register, name="register"),
    path("confirm-email/<email>/", views.confirm_email, name="confirm_email"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("authorization/", views.authorizations, name="authorizations"),
    path("logout/", views.log_out, name="logout"),
    path("new-password/<uidb64>/", views.new_password_view, name="new_password"),
]
