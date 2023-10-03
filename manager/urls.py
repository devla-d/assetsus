from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="admindashboard"),
    path("users/", views.users, name="users"),
    path("users/<int:pk>", views.user_detail, name="user_detail"),
    path("withdrawals/", views.withdrawal_, name="withdrawal_super"),
    path("users/<int:pk>/login/", views.login_user_account, name="login_user_account"),
    path("withdrawals/<int:pk>", views.withdrawal_detail, name="withdrawal_detail"),
    path("deposits/", views.deposit_, name="deposit_"),
    path("deposit/<int:pk>", views.deposit_details, name="deposit_details"),
    path("documents/", views.documents_, name="docs"),
    path("documents-details/<int:pk>/", views.documents_details, name="docs_details"),
    path("process-document/<int:pk>/", views.process_documents_, name="process_doc"),
    path("investments/", views.investments, name="investments"),
    path("investments/<int:pk>", views.investments_detail, name="investments_detail"),
    path("investments-topup/", views.investments_topup, name="investments_topup"),
]
