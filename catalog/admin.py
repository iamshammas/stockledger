from django.contrib import admin
from .models import Product, Category, Brand, Unit

admin.site.register([Product, Category, Brand, Unit])
