from django.contrib import admin

# Register your models here.

from inventory.models import Category, Asset, AssetInstance

# admin.site.register(Category)
# admin.site.register(Asset)
# admin.site.register(AssetInstance)

# # Define the admin class
class CategoryAdmin(admin.ModelAdmin):
    pass
# Register the admin class with the associated model
admin.site.register(Category, CategoryAdmin)

# Register the Admin classes for Asset using the decorator (does same thing as above with admin.site.register() )
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'model', 'display_category', 'condition', 'owner')

# Register the Admin classes for AssetInstance using the decorator (does same thing as above with admin.site.register() )
@admin.register(AssetInstance)
class AssetInstanceAdmin(admin.ModelAdmin):
    list_display = ('asset', 'uid', 'checked_out', 'return_date', 'borrower')
    list_filter = ('checked_out', 'return_date')

