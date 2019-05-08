from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse

import uuid

class Category(models.Model):
    """Model representing an Asset category"""

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Asset(models.Model):
    """Model representing an Asset"""

    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=64)
    model = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

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

    def __str__(self):
        return self.name

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(category.name for category in self.category.all())
    
    display_category.short_description = 'Category'

class AssetInstance(models.Model):
    # Unique identifier for an instance of an asset (a barcode of sorts)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # Each asset can have multiple copies; a copy only has one associated Asset
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True)
    checked_out = models.BooleanField(default=False)
    return_date = models.DateField(null=True, blank=True)
    borrower = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ['return_date']

    def __str__(self):
        return f'{self.uid} - {self.asset.name}'