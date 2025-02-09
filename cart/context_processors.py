"""
Create context processor so our cart can work on all pages of the site
"""
from .cart import Cart

def cart(request):
    """
    Return the default data from our Cart
    """
    return {'cart': Cart(request)}
