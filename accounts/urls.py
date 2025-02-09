"""
Module for the url paths in the accounts app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bestsellers/', views.bestsellers, name='bestsellers'),
    path('coming_soon/', views.coming_soon, name='coming_soon'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('register/', views.register_user, name='register'),
    path('book/<int:pk>', views.book, name='book'),
    path('search/', views.search, name='search'),
    path('book/<int:pk>/review/', views.book_review, name='book_review'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
]
