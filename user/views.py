from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accesscontrol.models import Kyc
from baseapp import utils
from django.contrib import messages

import pyotp

from user.models import Notification, Transactions, Packages, Investments

from .forms import DepositForm, KycForm, UpdateUserForm


@login_required()
def index(request):
    return render(request, "user/index.html")


@login_required()
def plan(request):
    packages = Packages.objects.all()
    return render(request, "user/plan.html", {"packages": packages})


@login_required()
def deposit(request):
    if request.POST:
        amount = int(request.POST.get("amount"))
        method = request.POST.get("mode")
        return redirect("confirm_deposit", amount=amount, mode=method)
    return render(request, "user/deposit.html")


@login_required()
def confirm_deposit(request, amount, mode):
    user = request.user
    if mode in utils.wallets and amount >= 700:
        if request.POST:
            form = DepositForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                form.save()

                messages.error(
                    request, "Deposit has been created it's now under reviewed "
                )

                return redirect("transactions")
        else:
            context = {
                "amount": amount,
                "mode": mode,
                "address": utils.ADMIN_ADDRESS[mode],
            }
            return render(request, "user/confirm_deposit.html", context)

    else:
        messages.error(request, "Invalid Link")
        return redirect("deposit_page")


@login_required()
def kyc(request):
    user = request.user
    try:
        doc = Kyc.objects.get(user=request.user)
    except Kyc.DoesNotExist:
        doc = None
    if request.POST:
        form = KycForm(request.POST, request.FILES)
        if form.is_valid():
            if doc:
                document_front = form.cleaned_data["document_front"]
                document_back = form.cleaned_data["document_back"]
                doc.document_front = document_front
                doc.document_back = document_back
                doc.user = user
                doc.status = "proccessing"
                doc.save()
                messages.info(request, ("Document Submited"))
                return redirect("kyc")
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            messages.info(request, ("Document Submited"))
            return redirect("kyc")
        else:
            messages.info(request, ("SOMETHING WENT WRONG"))
            return redirect("kyc")
    return render(request, "user/kyc.html", {"doc": doc})


@login_required()
def withdrawal(request):
    user = request.user
    if user.is_verified != True:
        messages.error(request, "Verify Your Account")
        return redirect("kyc")
    if request.POST:
        amount = int(request.POST.get("amount"))
        amount_in_coin = request.POST.get("amount_in_coin")
        mode = request.POST.get("mode")
        addr = utils.check_user_address(user)
        print(addr)
        if addr:
            if user.balance >= amount:
                transaction = Transactions(
                    user=user,
                    amount=amount,
                    amount_in_coin=amount_in_coin,
                    method=mode,
                    trans_type=utils.W,
                )
                user.balance -= amount
                user.save()
                transaction.save()

                messages.error(request, f"You just place a withdrawal of ${amount}")
                return redirect("withdrawal")
            else:
                messages.error(request, "Insuficient Funds")
                return redirect("withdrawal")
        else:
            messages.error(request, "Please Update your withdrawal addresses")
            return redirect("withdrawal")
    return render(request, "user/withdrawal.html")


@login_required()
def update_wallet_page(request):
    user = request.user
    if request.POST:
        btc_address = request.POST.get("btc_address")
        usdt_address = request.POST.get("usdt_address")
        eth_address = request.POST.get("eth_address")

        user.eth_address = eth_address
        user.usdt_address = usdt_address
        user.btc_address = btc_address

        user.save()
        messages.error(request, "Wallet Updated succesfully")
        return redirect("update_wallet_page")

    return render(request, "user/update_wallet.html")


@login_required()
def transactions(request):
    transactions = Transactions.objects.filter(user=request.user).order_by("-date")
    return render(request, "user/transactions.html", {"transactions": transactions})


@login_required()
def referrals(request):
    return render(request, "user/referal.html")


@login_required()
def profile(request):
    user = request.user
    if request.POST:
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.error(request, "Account updated")
            return redirect("profile")
        else:
            messages.error(request, "Error in form field")
            return redirect("profile")
    return render(request, "user/profile.html")


@login_required()
def invest_static(request):
    user = request.user
    investments = Investments.objects.filter(user=user).order_by("-date")
    tot_amount_invested = utils.get_total_investment_by_user(Investments, user)
    print(tot_amount_invested)
    context = {"tot_amount_invested": tot_amount_invested, "investments": investments}
    return render(request, "user/invest_static.html", context)


@login_required()
def create_investment_page(request):
    user = request.user
    if request.POST:
        pack_id = int(request.POST.get("plan_id"))
        amount = int(request.POST.get("amount"))

        package = get_object_or_404(Packages, pk=pack_id)
        if amount >= package.min_amount or amount <= package.max_amount:
            if user.deposit_balance >= amount:
                investment = Investments(
                    user=user,
                    amount_invested=amount,
                    end_date=utils.get_deadline(package.duration),
                    package=package,
                )
                user.deposit_balance -= amount
                investment.save()
                user.save()
                messages.error(request, "Investment Created succesfully")
                return redirect("invest_static")
            else:
                messages.error(request, "Insuficient Funds Please Deposit")
                return redirect("plan")
        else:
            messages.error(
                request,
                "Please make sure the amount corresponds with the plans minimum and maximuim amount",
            )
            return redirect("plan")
    else:
        messages.info(request, "SOMETHING WENT WRONG")
        return redirect("plan")


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
