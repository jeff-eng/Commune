from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import date
from django.urls import reverse

import uuid

class Category(models.Model):
    """Model representing an Asset category"""
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Borrower(models.Model):
    """Model representing a Borrower"""
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    associated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Asset(models.Model):
    """Model representing an Asset"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=64)
    model = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=12)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, null=True, blank=True)
    checked_out = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)    

    CONDITION_TYPE = (
        ('e', 'Excellent'),
        ('g', 'Good'),
        ('f', 'Fair'),
        ('p', 'Poor'),
    )
    
    condition = models.CharField(
        max_length=1,
        choices=CONDITION_TYPE,
        blank=True,
        help_text='Asset condition')

    class Meta:
            ordering = ['return_date']

    @property
    def is_dueback(self):
        if self.return_date and date.today() > self.return_date:
            return True
        return False
    
    @property
    def borrower_name(self):
        if self.borrower is not None:
            return f'{self.borrower.first_name} {self.borrower.last_name}'
        return 'None'
    
    @property
    def formatted_return_date(self):
        if self.return_date:
            return f'{self.return_date}'

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return self.category.name
    
    display_category.short_description = 'Category'

    def __str__(self):
        return f'{self.uid} - {self.name}'

    def get_absolute_url(self):
        return reverse('asset-detail', args=[str(self.uid)])