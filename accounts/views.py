"""
Views for the accounts app.
"""
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from .forms import SignUpForm, UpdateUserForm, UserInfoForm
from .models import Book, Customer, ProductReviews, Profile


# Create your views here.

def home(request: HttpRequest)-> HttpResponse:
    """
    Renders the home page, displaying all available books.
    """
    books = Book.objects.all()
    return render(request, 'accounts/dashboard.html', {'books':books})

def bestsellers(request: HttpRequest) -> HttpResponse:
    """
    Renders the bestsellers page, displaying all bestselling books.
    """
    books = Book.objects.all()
    return render(request, 'accounts/bestsellers.html', {'books':books})

def coming_soon(request: HttpRequest) -> HttpResponse:
    """
    Renders the coming_soon page, displaying all coming soon books.
    """
    books = Book.objects.all()
    return render(request, 'accounts/coming_soon.html', {'books':books})

def login_user(request: HttpRequest) -> HttpResponse:
    """
    Handles user login. Authenticates the user.
    Users can save their shopping carts between sessions,
    and when they log in again, their previous cart items are
    automatically loaded into the current session cart.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user.id)

            current_user = Customer.objects.get(user__id = request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database str to dict
            if saved_cart:
                # Convert to dict using json
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dict to session
                cart = Cart(request)
                # Loop through the cart(dict) and add the items from the database
                for key, value in converted_cart.items():
                    cart.add(book=key, quantity=value, db_add=True)

            messages.success(request, ("You have been logged in!"))
            return redirect('home')

        messages.success(request, ("There was an error, please try again!"))
        return redirect('login')

    return render(request, 'accounts/login.html')

def logout_user(request: HttpRequest) -> HttpResponse:
    """
    Logs out the current user and redirects them to the home page.
    """
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration. Validates and saves the user's information, 
    creates a new Customer object, and redirects to the update info page.
    """
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            #log in user
            user = authenticate(username=username,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                email=email
                                )
            customer = Customer.objects.create(user=user, password=password, email=email)
            login(request, user)
            messages.success(request, ("Username created - please fill out user information below"))
            return redirect('update_info')

        messages.success(request, ("Whoops! There was a problem registering, please try again"))
        return redirect('register')

    return render(request, 'accounts/register.html', {'form':form})

def update_user(request: HttpRequest) -> HttpResponse:
    """
    Allows the authenticated user to update existing details.
    """
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated!")
            return redirect('home')
        return render(request, 'accounts/update_user.html', {'user_form': user_form})

    messages.success(request, "You must be logged in to access that page!")
    return redirect('home')

def update_info(request: HttpRequest) -> HttpResponse:
    """
    Allows the authenticated user to update their user info and shipping address. 
    """
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your information has been updated!")
            return redirect('home')
        return render(request, 'accounts/update_info.html',
                        {'form': form, 'shipping_form':shipping_form})

    messages.success(request, "You must be logged in to access that page! ")
    return redirect('home')

def book(request: HttpRequest, pk: int) -> HttpResponse:
    """
     Renders the book details page for a specific book identified by its primary key.
    """
    book_details = Book.objects.get(id=pk)
    return render(request, 'accounts/book.html', {'book':book_details})

def search(request: HttpRequest) -> HttpResponse:
    """
    Handles search functionality for books based on the search term entered by the user.
    User can serach by title or tag
    """
    if request.method == "POST":
        searched = request.POST['searched']
        searched_books = Book.objects.filter(
            Q(title__icontains=searched) |
            Q(tags__name__icontains=searched)
        ).distinct()
        if not searched_books:
            return render(request, 'accounts/search.html', {})

        return render(request, 'accounts/search.html',
                          {'searched':searched, 'searched_books':searched_books})

    return render(request, 'accounts/search.html', {})

def book_review(request: HttpRequest, pk: int) -> JsonResponse:
    """
    Allows a logged-in user to submit or update a review for a specific book. 
    Returns a JSON response with the review details.
    """
    book = Book.objects.get(id=pk)
    user = request.user
    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')
        review = None

        existing_review = ProductReviews.objects.filter(book=book, user=user).first()
        if existing_review:
            existing_review.content = content
            existing_review.stars = stars
            existing_review.save()
            review = existing_review
            messages.info(request, "Your review has been updated.")
        else:
            review = ProductReviews.objects.create(
                book=book,
                user=user,
                stars=stars,
                content=content)
            messages.success(request, "Review submitted successfully!")

        response_data = {
            'message': 'Review submitted successfully!',
            'stars': review.stars,
            'content': review.content,
            'user': request.user.username,
            'date_created': review.data_created.strftime('%Y-%m-%d') 
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def recommendations_view(request: HttpRequest) -> HttpResponse:
    """
    Provides book recommendations for a logged-in user based on collaborative filtering 
    using ratings data. If the user has not rated any books, generic recommendations are provided.
    """
    if not request.user.is_authenticated:
        # Redirect and show a message if the user is not authenticated
        return render(request, 'login.html',
                      {'message': 'You need to be logged in to view recommendations.'})

    user = request.user  # Get the logged-in user

    # all ratings data for the current user
    ratings = ProductReviews.objects.filter(user=user)

    if not ratings.exists():
        # Handle case where the user has no ratings
        return HttpResponse("No ratings found for this user. Please rate some books first.")

    all_books = Book.objects.all().values_list('id', flat=True)
    all_ratings = ProductReviews.objects.all()  # Fetch ratings for all users
    all_users = list(User.objects.all().values_list('username', flat=True))

    ratings_matrix = pd.DataFrame(np.nan, index=all_users, columns=all_books)

    # For each rating, we update the corresponding cell in the DataFrame
    for rating in all_ratings:
        ratings_matrix.loc[rating.user.username, rating.book.id] = rating.stars

    # Now `ratings_matrix` will have `NaN` for unrated books and actual ratings where applicable
    ratings_matrix = ratings_matrix.fillna(0)

    # Calculate similarity between books (item-based collaborative filtering)
    item_similarity = cosine_similarity(ratings_matrix.T)

    # Create a DataFrame for item similarities (book-to-book similarities)
    item_similarity_df = pd.DataFrame(item_similarity,
                                      index=ratings_matrix.columns,
                                      columns=ratings_matrix.columns
                                    )

    # Get the books the user has rated
    user_ratings = ratings_matrix.loc[user.username]
    rated_books = user_ratings[user_ratings > 0].index.tolist()
    #print(f"Books rated by {user.username}: {rated_books}")

    if not rated_books:
    # If the user hasn't rated any books yet,return a generic set of recommendations
        recommended_books = Book.objects.all()[:3]  # first 3 books
        return render(request, 'accounts/recommendations.html',
                      {'recommended_books': recommended_books})

    # Get the similarity scores of the rated books
    similar_scores = item_similarity_df.loc[rated_books].mean(axis=0)
    # Exclude books the user has already rated
    similar_scores = similar_scores.drop(rated_books)
    # Sort and select top 3 book recommendations
    recommended_books_ids = similar_scores.sort_values(ascending=False).head(3).index.tolist()
    recommended_books = Book.objects.filter(id__in=recommended_books_ids)

    # Render the recommendations in the template
    return render(request, 'accounts/recommendations.html',
                  {'recommended_books': recommended_books}
                )
