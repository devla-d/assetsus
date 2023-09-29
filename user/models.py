from django.db import models

from accesscontrol.models import Account
from baseapp import utils


class Notification(models.Model):
    user = models.ForeignKey(
        Account, related_name="user_notify", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} "


class Transactions(models.Model):
    user = models.ForeignKey(
        Account,
        related_name="user_transactions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    amount = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=40, default="pending")
    trans_type = models.CharField(max_length=50)
    method = models.CharField(max_length=50)
    unique_u = models.CharField(max_length=30, blank=True, null=True, unique=True)
    prove_img = models.ImageField(upload_to="prove/", blank=True, null=True)
    amount_in_coin = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} :  {self.trans_type}"

    def save(self, *args, **kwargs):
        # Perform custom logic before saving
        if self.unique_u is None or self.unique_u == "":
            self.unique_u = utils.gen_random_code(6)

        # Call parent save method
        super().save(*args, **kwargs)


STATUS = (
    ("active", "active"),
    ("inactive", "inactive"),
    ("pending", "pending"),
    ("completed", "completed"),
)


class Packages(models.Model):
    duration = models.IntegerField()
    name = models.CharField(max_length=40)
    roi = models.IntegerField()
    min_amount = models.IntegerField(default=0)
    max_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Investments(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount_invested = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=40, choices=STATUS, default="active")
    amount_earn = models.IntegerField(default=0)
    package = models.ForeignKey(
        Packages, on_delete=models.CASCADE, related_name="pack", blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} :  {self.amount_invested}"
