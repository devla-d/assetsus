from django import forms
from .models import Transactions
from accesscontrol.models import Account, Kyc


class DepositForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ["amount", "method", "prove_img", "trans_type", "amount_in_coin"]


class KycForm(forms.ModelForm):
    class Meta:
        model = Kyc
        fields = [
            "document_front",
            "document_back",
        ]


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "last_name",
            "first_name",
            "country",
            "city",
            "address",
            "zipcode",
        ]
