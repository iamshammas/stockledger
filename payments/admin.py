from django.contrib import admin

from .models import Payment, RetailerCredit

admin.site.register(Payment)
admin.site.register(RetailerCredit)