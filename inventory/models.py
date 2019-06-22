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

class Borrower(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Asset(models.Model):
    """Model representing an Asset"""
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=64)
    model = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, null=True)
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
        help_text='Asset condition'
    )

    class Meta:
            ordering = ['return_date']

    @property
    def is_dueback(self):
        if self.return_date and date.today() > self.return_date:
            return True
        return False

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(category.name for category in self.category.all())
    
    display_category.short_description = 'Category'

    def get_absolute_url(self):
        return reverse('asset-detail', args=[str(self.uid)])
    
    def __str__(self):
        return f'{self.uid} - {self.name}'