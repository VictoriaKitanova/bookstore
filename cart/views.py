"""
The module includes functionality for displaying the cart summary, adding/removing books, 
and updating the cart quantities.
"""
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import Book
from .cart import Cart

# Create your views here.

def cart_summary(request: HttpRequest) -> HttpResponse:
    """
    Displays the cart summary page with the books in the cart, their quantities, and total price.
    """
    # Get the cart
    cart = Cart(request)
    cart_books = cart.get_books
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html",
                  {'cart_books': cart_books,
                   "quantities": quantities,
                   "totals":totals}
                )

def cart_add(request: HttpRequest) -> JsonResponse:
    """
    Adds a book to the cart
    """
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        book_id = int(request.POST.get('book_id'))
        book_qty = int(request.POST.get('book_qty'))
        # lookup book in DB
        book = get_object_or_404(Book, id=book_id)
        # Save to session
        cart.add(book=book, quantity=book_qty)
        # Return response
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty ': cart_quantity})
        messages.success(request, ("Book added to your cart!"))
        return response

    return redirect('home')

def cart_delete(request: HttpRequest) -> JsonResponse:
    """
    Deletes a book from the cart
    """
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        book_id = int(request.POST.get('book_id'))
        # Call delete function in Cart
        cart.delete(book=book_id)

        response = JsonResponse({'book': book_id})
        messages.success(request, ("Book deleted from your cart"))
        return response

    return redirect('home')


def cart_update(request: HttpRequest) -> JsonResponse:
    """
    Updates the quantity of a book in the cart
    """
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        book_id = int(request.POST.get('book_id'))
        book_qty = int(request.POST.get('book_qty'))

        cart.update(book=book_id, quantity=book_qty)

        response = JsonResponse({'qty': book_qty})
        messages.success(request, ("Your cart has been updated"))
        return response

    return redirect('home')
