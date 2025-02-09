"""
Models for the accounts app.

This module defines the models used in the accounts app, including user profiles,
customers, books, tags, orders, and product reviews
"""
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    """
    Model for storing user profile information.

    This model extends the default User model to store additional information
    about the user such as phone number, address, city, and country. It also 
    tracks when the profile data was last modified.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_modified = models.DateTimeField(auto_now_add=True, null=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    """
    Create a user Profile by default when user signs up
    """
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender = User)

class Customer(models.Model):
    """
    Model for storing customer information.

    This model stores details about customers, including their phone number, 
    email, password, and any old cart data. It is linked to the User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    old_cart = models.CharField(max_length=200, blank = True, null=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    """
    Model for storing book tags.

    This model is used to categorize books by tags, allowing books to be
    associated with one or more tags for easir searching.
    """
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    """
    Model for storing book information.

    This model stores details about books, such as the title, author, price, 
    publication date, number of pages, cover, description, and associated tags. 
    It also includes an image field for the book's cover.
    """
    title = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    publication = models.DateField(default=datetime.date.today)
    pages = models.IntegerField(default=0, null=True)
    cover = models.CharField(max_length=10, null=True)
    descreption = models.CharField(max_length=10000, default='', blank=True, null=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='static/images/', default='')

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):
    """
    Model for storing customer orders.
    """
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    data_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

class ProductReviews(models.Model):
    """
    Model for storing product reviews.

    This model allows users to leave reviews. 
    Each review includes a star rating and optional content. A unique constraint 
    ensures that a user can only leave one review per book.
    """
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    data_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Enforce unique review per user per book and don't plurarize reviews
        """
        unique_together = ['book', 'user']
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return f"Review by {self.user} for {self.book.title}"
