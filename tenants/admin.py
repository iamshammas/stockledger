from django.contrib import admin
from .models import SellerProfile, Tenant

admin.site.register([SellerProfile, Tenant])