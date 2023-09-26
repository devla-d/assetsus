from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Kyc


User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username"]
    list_filter = ["is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "country",
                    "gender",
                    "zipcode",
                    "city",
                    "region",
                    "address",
                    "date_of_birth",
                    "phone",
                    "unique_id",
                )
            },
        ),
        (
            ("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            ("Balance"),
            {
                "fields": (
                    "balance",
                    "deposit_balance",
                    "total_withdraw",
                    "referral_bonus",
                    "referral",
                    "btc_address",
                    "eth_address",
                    "usdt_address",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


admin.site.register(Kyc)
