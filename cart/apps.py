"""
This module contains the configuration for the cart app 
"""
from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Configuration class for the cart app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
