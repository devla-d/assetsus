import random
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum

from datetime import timedelta
from uuid import uuid4
import qrcode

from io import BytesIO


import pyotp

from base64 import b64encode


def generate_totp_secret():
    return pyotp.random_base32()


def generate_qr_code(secret, user):
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        user.username, issuer_name="Assetsus"
    )

    img = qrcode.make(totp_uri)
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code = f"data:image/png;base64,{encoded_img}"
    return qr_code


EMAIL_ADMIN = settings.DEFAULT_FROM_EMAIL
D = "deposit"
W = "withdraw"

ADMIN_ADDRESS = {
    "BTC": "bc1qctg5j7ky9fmsepvhe098zegsyf2yjvwfnxy38u",
    "ETH": "0x82A0DBA5Adad195C322d35593F7099F9E55F1461",
    "USDT": "0x82A0DBA5Adad195C322d35593F7099F9E55F1461",
    "BNB": "bnb1tyrv5ruc6zdgpkkx6q0r3tzlp0wy62mhpvudp0",
}
wallets = ["BTC", "ETH", "USDT", "BNB"]


def gen_random_number():
    return str(random.randint(100000, 999999))


# def set_expirable_var(session, var_name, value, expire_at):
#     session[var_name] = {'value': value, 'expire_at': expire_at.timestamp()}

# def get_expirable_var(session, var_name, default=None):
#     var = default
#     if var_name in session:
#         my_variable_dict = session.get(var_name, {})
#         if my_variable_dict.get('expire_at', 0) > datetime.now().timestamp():
#             var = my_variable_dict.get('value')
#         else:
#             del session[var_name]
#     return var


# def verify_exp():
#     return timezone.now() + timedelta(minutes=10)


def gen_random_code(len):
    code = str(uuid4()).replace(" ", "-").upper()[:len]
    return code


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_next_destination(request):
    next = None
    if request.GET.get("next"):
        next = str(request.GET.get("next"))
    return next


def get_deadline(days):
    return timezone.now() + timedelta(days=days)


def earnings(amount, perc):
    p = (perc / 100) * amount
    return p + amount


def create_notification(**info):
    """
    Create A New notification Object
    """
    notification = info["model"](
        user=info["user"], title=info["title"], body=info["body"]
    )
    notification.save()
    return notification


def trans_code():
    code = str(uuid4()).replace(" ", "-").upper()[:8]
    return code


def check_user(email, model):
    account = None
    try:
        account = model.objects.get(email__exact=email)
    except model.DoesNotExist:
        account = None

    return account


def check_user_username(username, model):
    account = None
    try:
        account = model.objects.get(username__exact=username)
    except model.DoesNotExist:
        account = None

    return account


def check_user_address(user):
    return all([user.btc_address, user.eth_address, user.usdt_address])


def get_user_address(user, method):
    address = None
    if method == "BTC":
        address = user.btc_address
    elif method == "ETH":
        address = user.eth_address
    elif method == "USDT":
        address = user.usdt_address
    else:
        address = None

    return address


def get_total_investment_by_user(cls, user):
    total_investment = cls.objects.filter(user=user).aggregate(Sum("amount_invested"))[
        "amount_invested__sum"
    ]
    if total_investment is None:
        total_investment = 0
    return total_investment


def get_total_adeposit_by_user(cls, user):
    total_deposit = cls.objects.filter(user=user, status="approved").aggregate(
        Sum("amount")
    )["amount__sum"]
    if total_deposit is None:
        total_deposit = 0
    return total_deposit


def get_user_balance(user, ty_pe):
    bal = 0
    if ty_pe == 1:
        bal = user.balance
    elif ty_pe == 2:
        bal = user.referral_bonus
    else:
        bal = 0
    return int(bal)


def deduct_user_balance(user, ty_pe, amount_dedut):
    bal = 0
    if ty_pe == 1:
        user.balance -= amount_dedut
        user.save()
        bal = user.balance
    elif ty_pe == 2:
        user.referral_bonus -= amount_dedut
        user.save()
        bal = user.referral_bonus
    else:
        bal = 0
    return int(bal)
