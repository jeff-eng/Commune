from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import date

class Asset(models.Model):
    # properties
    name = models.CharField(max_length=200)
    make = models.CharField(max_length=64)
    model = models.CharField(max_length=128)
    description = models.TextField()
    serial_number = models.CharField(max_length=128)
    borrower = models.CharField(max_length=128)
    checkout_date = models.DateField(auto_now=True)
    return_date = None
    checked_out = models.BooleanField(default=False)

    # methods
    def check_out(self):
        self.checked_out = True
        self.checkout_date = date.today()
        self.save()
        print("Checked out.")

    def return_asset(self):
        self.checked_out = False
        self.checkout_date = None
        self.return_date = None

    def __str__(self):
        return self.name
