"""
Django Admin configuration for managing models in the admin interface.
"""
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Customer, Book, Tag, Order, ProductReviews, Profile

admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(ProductReviews)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    """
    Mix profile info and user info
    """
    model = Profile

class UserAdmin(admin.ModelAdmin):
    """
    Extend the user model
    """
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User, UserAdmin)
