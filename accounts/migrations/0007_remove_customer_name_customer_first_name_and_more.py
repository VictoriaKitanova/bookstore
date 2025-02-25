# Generated by Django 5.1.4 on 2025-01-03 15:57
"""
Module for 7 migration 
"""
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Seventh migration
    """
    dependencies = [
        ('accounts', '0006_remove_order_tags_book_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='descreption',
            field=models.CharField(blank=True, default='', max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
