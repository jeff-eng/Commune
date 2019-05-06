from django.contrib import admin

# Register your models here.

from inventory.models import Category, Asset, AssetInstance

admin.site.register(Category)
admin.site.register(Asset)
admin.site.register(AssetInstance)