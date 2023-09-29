from django.contrib import admin
from .models import Transactions, Packages, Investments, Notification


admin.site.register(Transactions)
admin.site.register(Packages)
admin.site.register(Investments)
admin.site.register(Notification)
