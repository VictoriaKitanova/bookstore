# Generated by Django 5.1.4 on 2025-01-02 12:25
"""
Module for 3 migration 
"""
from django.db import migrations


class Migration(migrations.Migration):
    """
    Third migration
    """
    dependencies = [
        ('accounts', '0002_order_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='Book',
        ),
    ]
