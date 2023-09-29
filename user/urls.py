from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.index, name="dashboard"),
    path("twofactor/", views.enable_2fa, name="enable_2fa"),
    path("disable-twofactor/", views.disable_2fa, name="disable_2fa"),
    path("plans/", views.plan, name="plan"),
    path("deposit-funds/", views.deposit, name="deposit"),
    path(
        "deposit-funds/confirm//<int:amount>/<str:mode>/",
        views.confirm_deposit,
        name="confirm_deposit",
    ),
    path("kyc-form/", views.kyc, name="kyc"),
    path("transaction-logs/", views.transactions, name="transactions"),
    path("withdraw-funds/", views.withdrawal, name="withdrawal"),
    path("referrals/", views.referrals, name="referrals"),
    path("profile/", views.profile, name="profile"),
    path("investments/", views.invest_static, name="invest_static"),
    path("update-wallet-address/", views.update_wallet_page, name="update_wallet_page"),
]
