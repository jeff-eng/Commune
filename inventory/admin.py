from django.contrib import admin

# Register your models here.

from inventory.models import Category, Asset, Borrower

# Define the admin class
class CategoryAdmin(admin.ModelAdmin):
    pass
# Register the admin class with the associated model
admin.site.register(Category, CategoryAdmin)

# Register the Admin classes for Asset using the decorator (does same thing as above with admin.site.register() )
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('uid', 
                    'name', 
                    'manufacturer', 
                    'model', 
                    'display_category', 
                    'condition', 
                    'checked_out', 
                    'return_date',
                    'is_dueback', 
                    'owner', 
                    'borrower')
    list_filter = ('checked_out', 'return_date')

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'associated_user')