from django.contrib import admin
from inventory.models import Category, Asset, Borrower

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
    )

# Register the Admin classes for Asset using the decorator (does same thing as above with admin.site.register() )
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('uid',
                    'name', 
                    'display_category',
                    'checked_out', 
                    'return_date',
                    'is_dueback', 
                    'owner', 
                    'borrower'
    )
    list_filter = ('checked_out', 
                   'return_date'
    )

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'first_name', 
                    'last_name', 
                    'associated_user'
    )