"""
Manages the shopping cart functionality
"""
from accounts.models import Book, Customer

class Cart():
    """
    A shopping cart for a user, handling the cart's items, their quantities, 
    and the total price. For logged-in users.
    """
    def __init__(self, request):
        """
        Initializes the cart using session data. If no session key exists, creates one.
        """
        self.session = request.session
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key. Create one.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of the site
        self.cart = cart

    def add(self, book, quantity, db_add=False):
        """
        Adds a book to the cart. Saves cart data for logged-in users.
        """
        if db_add:
            book_id = str(book)
        else:
            book_id = str(book.id)
        book_qty = str(quantity)

        if book_id not in self.cart:
            self.cart[book_id] = int(book_qty)

        self.session.modified = True

        # Deal with logged in user:
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Customer.objects.filter(user__id = self.request.user.id)
            # Convert { '3': 1, '2': 2} to {"3": 1, "2": 2} bc json from str to dict
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save our carty to the customer model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        """
        Returns the number of items in the cart.
        """
        return len(self.cart)

    def get_books(self):
        """
         Returns the books currently in the cart.
        """
        # Get ids from cart
        books_ids = self.cart.keys()
        # Use ids to lookup products in the DB model
        books = Book.objects.filter(id__in=books_ids)
        # Return those looked up products
        return books

    def get_quants(self):
        """
        Returns the quantities of books in the cart.
        """
        quantities = self.cart
        return quantities

    def update(self, book, quantity):
        """
        Updates the quantity of a book in the cart.
        Args:
            book (Book): The book to update.
            quantity (int): The new quantity.
        
        Returns:
            dict: Updated cart.
        """
        book_id = str(book)
        book_qty = int(quantity)

        ourcart = self.cart
        ourcart[book_id] = book_qty

        self.session.modified = True

        # for the change in old_cart in our admin when we update the book/s
        current_user = Customer.objects.filter(user__id = self.request.user.id)
        carty = str(self.cart)
        carty = carty.replace("\'", "\"")
        # Save our carty to the customer model
        current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing

    def delete(self, book):
        """
        Removes a book from the cart.
        """
        book_id = str(book)
        # Delete from dictionary/cart
        if book_id in self.cart:
            del self.cart[book_id]

        # for the change in old_cart in our admin when we delete the book/s
        current_user = Customer.objects.filter(user__id = self.request.user.id)
        carty = str(self.cart)
        carty = carty.replace("\'", "\"")
        # Save our carty to the customer model
        current_user.update(old_cart=str(carty))

        self.session.modified = True

    def cart_total(self):
        """
        Calculates the total price of items in the cart.
        """
        # Get books IDs
        book_ids = self.cart.keys()
        # Lookup those keys in our book database model
        books = Book.objects.filter(id__in=book_ids)
        # Get quantities
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            #{'4':3, '2':1}
            key = int(key)
            for book in books:
                if book.id == key:
                    total = total + (book.price * value)
        return total
