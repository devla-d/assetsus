from django.db import models
from django.contrib.auth.models import AbstractUser


from baseapp import utils


class Account(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    zipcode = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    address = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)

    date_of_birth = models.CharField(max_length=100, blank=True, null=True)

    phone = models.CharField(max_length=30, blank=True, null=True)
    balance = models.IntegerField(default=0, blank=True, null=True)
    deposit_balance = models.IntegerField(default=0, blank=True, null=True)

    total_withdraw = models.IntegerField(default=0, blank=True, null=True)
    is_updated = models.BooleanField(default=False)
    referral_bonus = models.IntegerField(default=0, blank=True, null=True)
    referral = models.IntegerField(default=0, blank=True, null=True)

    unique_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)

    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)

    btc_address = models.CharField(max_length=100, blank=True, null=True)
    eth_address = models.CharField(max_length=100, blank=True, null=True)
    usdt_address = models.CharField(max_length=100, blank=True, null=True)

    otp_secret_key = models.CharField(max_length=64, blank=True, null=True)
    otp_enabled = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def image_url(self):
        if self.profile_image:
            return f"http://localhost:8000/{self.profile_image.url}"
        else:
            return f"https://ui-avatars.com/api/?name={self.get_fullname()}"

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def format_balance(self):
        return "{:,}".format(self.balance)

    def __str__(self):
        return self.email


class Kyc(models.Model):
    user = models.OneToOneField(
        Account,
        related_name="user_kyc",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    document_front = models.ImageField(blank=True, null=True, upload_to="document")
    document_back = models.ImageField(blank=True, null=True, upload_to="document")
    is_approved = models.BooleanField(default=False)
    status = models.CharField(default="proccessing", max_length=50)
