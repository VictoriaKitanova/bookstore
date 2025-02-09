"""
This module contains views for handling the payment and checkout process
"""
import datetime
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from accounts.models import Customer
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem


def payment_success(request: HttpRequest) -> HttpResponse:
    """
    Renders a success page after successful payment.
    """
    return render(request, "payment/payment_success.html", {})

def checkout(request: HttpRequest) -> HttpResponse:
    """
    Handles the checkout process for both authenticated users and guests.
    """
    # Get the cart
    cart = Cart(request)
    cart_books = cart.get_books
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html",
                      {'cart_books': cart_books,
                       "quantities": quantities,
                       "totals":totals,
                       "shipping_form":shipping_form}
                    )

    # Checkout as guest
    shipping_form = ShippingForm(request.POST or None)
    return render(request, "payment/checkout.html",
                    {'cart_books': cart_books,
                    "quantities": quantities,
                    "totals":totals,
                    "shipping_form":shipping_form}
                )

def billing_info(request: HttpRequest) -> HttpResponse:
    """
    Handles the billing information form for the order process.
    """
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_books = cart.get_books
        quantities = cart.get_quants
        totals = cart.cart_total()
        my_shipping = request.POST
        # create a session with shipping info
        request.session['my_shipping'] = my_shipping

        # get the billing form
        billing_form = PaymentForm(request.POST)
        return render(request, "payment/billing_info.html",
                    {'cart_books': cart_books,
                        'quantities': quantities,
                        'totals': totals,
                        'shipping_info': request.POST,
                        'billing_form': billing_form
                        })

    messages.success(request, "Access denied")
    return redirect('home')

def process_order(request: HttpRequest) -> HttpResponse:
    """
    Processes the order, saves the order and its items, and clears the cart.
    """
    if not request.POST:
        messages.success(request, "Access denied")
        return redirect('home')

    # Get the cart
    cart = Cart(request)
    cart_books = cart.get_books
    quantities = cart.get_quants
    totals = cart.cart_total()

    # Get billing info from the last page
    payment_form = PaymentForm(request.POST or None)
    # Get shipping session data
    my_shipping = request.session.get('my_shipping')
    if not my_shipping:
        messages.error(request, "Shipping information is missing!")
        return redirect('home')

    # gather order info - the rest of the stuff from the order model
    full_name = my_shipping['shipping_full_name']
    email = my_shipping['shipping_email']
    # create shipping address from session info
    shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_country']}"
    amount_paid = totals

    # Determine if the user is logged in
    user = request.user if request.user.is_authenticated else None

    # Create order (whether logged in or not)
    order_data = {
        'full_name': full_name,
        'email': email,
        'shipping_address': shipping_address,
        'amount_paid': amount_paid
    }

    if user:
        # Logged-in user
        order_data['user'] = user
        create_order = Order.objects.create(**order_data)
        # Save cart items (order items)
        create_order_items(create_order, cart_books, quantities, user)
        clear_user_cart(user)
    else:
        # Guest user
        create_order = Order.objects.create(**order_data)
        create_order_items(create_order, cart_books, quantities)

    # Clear session and cart
    clear_session_cart(request)
    messages.success(request, "Order placed successfully!")
    return redirect('home')

def create_order_items(order, cart_books, quantities, user=None):
    """
    Helper function for process_order to create order items based on cart books and quantities.
    """
    for book in cart_books():
        book_id = book.id
        book_price = book.price
        for key, value in quantities().items():
            if int(key) == book.id:
                OrderItem.objects.create(
                    order=order,
                    book_id=book_id,
                    user=user,
                    quantity=value,
                    price=book_price
                )

def clear_user_cart(user):
    """
    Helper function for process_order to clear the old cart from the database.
    """
    current_user = Customer.objects.filter(user__id=user.id)
    current_user.update(old_cart="")


def clear_session_cart(request):
    """
    Helper function for process_order to clear the cart from the session.
    """
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

def shipped_dash(request: HttpRequest) -> HttpResponse:
    """
    Admin-only view for managing shipped orders.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # grab date and time
            now = datetime.datetime.now()
            # get the order
            order = Order.objects.filter(id=num)
            # update order
            order.update(shipped=False)
            # redirect
            messages.success(request, "Shipping status updated")
            return redirect('home')
        return render(request, "payment/shipped_dash.html", {"orders":orders})

    messages.success(request, "Access denied")
    return redirect('home')

def not_shipped_dash(request: HttpRequest) -> HttpResponse:
    """
    Admin-only view for managing orders that are not yet shipped.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        orders_obj = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # grab date and time
            now = datetime.datetime.now()
            # get the order
            order = Order.objects.filter(id=num)
            # update order
            order.update(shipped=True, date_shipped=now)
            # redirect
            messages.success(request, "Shipping status updated")
            return redirect('home')
        return render(request, "payment/not_shipped_dash.html", {"orders":orders_obj})

    messages.success(request, "Access denied")
    return redirect('home')

def orders(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Admin-only view to view and update an individual order's shipping status.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order
        order = Order.objects.get(id=pk)
        # get the orders items
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            # check if true or false
            if status == "true":
                # get the order
                order = Order.objects.filter(id=pk)
                # update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Shipping status updated")
            return redirect('home')

        return render(request, 'payment/orders.html', {"order":order, "items":items})

    messages.success(request, "Access denied")
    return redirect('home')
