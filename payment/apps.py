"""
This module contains the configuration for the payment app
"""
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """
    Configuration class for the payment ap
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
