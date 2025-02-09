"""
This module contains models related to order processing system.
"""
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import Book

class ShippingAddress(models.Model):
    """
    Represents the shipping address for an order.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)

    class Meta:
        """
        Don't plurarize address
        """
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        """
        Returns a string representation of the shipping address using its id
        """
        return f'Shipping Address - {str(self.id)}'

def create_shipping(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create an instance of 
    ShippingAddress when a new User is created.
    """
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender = User)

class Order(models.Model):
    """
    Represents an order placed by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'

@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    """
    Signal handler to set the shipping date when an order is marked as shipped. 
    Auto add shipping date
    """
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now

class OrderItem(models.Model):
    """
    Represents the items in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1, )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'
