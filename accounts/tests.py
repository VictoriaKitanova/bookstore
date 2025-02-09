"""
Module for testing the forms.
"""
import json
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.messages import get_messages
from cart.cart import Cart
from .forms import UserInfoForm, UpdateUserForm
from .models import Profile, Customer, Book, Tag, ProductReviews

class UserInfoFormTest(TestCase):
    """
    Test case for validating the UserInfoForm in different scenarios.
    """
    def test_user_info_form_valid(self):
        """
        Test that the UserInfoForm is valid when optional fields are filled.
        """
        form_data = {
            'phone': '1234567890',  # valid phone number
            'address': 'Street Nikola Genadiev',
            'city': 'Sofia',
            'country': 'Bulgaria'
        }
        form = UserInfoForm(data=form_data)
        self.assertTrue(form.is_valid())  #The form should be valid

    def test_user_info_form_invalid(self):
        """
        Test that the UserInfoForm is invalid when phone field is incorrectly formatted.
        """
        form_data = {
            'phone': 'NotANumber',  # invalid phone number
            'address': 'Street Nikola Genadiev',
            'city': 'Sofia',
            'country': 'Bulgaria'
        }
        form = UserInfoForm(data=form_data)
        self.assertFalse(form.is_valid())  # The form should be invalid due to invalid phone number

    def test_user_info_form_empty(self):
        """
        Test that the UserInfoForm is valid when all fields are left empty
        """
        form_data = {
            'phone': '',
            'address': '',
            'city': '',
            'country': ''
        }
        form = UserInfoForm(data=form_data)
        self.assertTrue(form.is_valid())  # The form should be valid because all fields are optional

    def test_user_info_form_placeholder(self):
        """
        Test that the form has the correct placeholders.
        """
        form = UserInfoForm()
        self.assertIn('placeholder="Phone"', str(form['phone']))
        self.assertIn('placeholder="Address"', str(form['address']))
        self.assertIn('placeholder="City"', str(form['city']))
        self.assertIn('placeholder="Country"', str(form['country']))


class UpdateUserFormTest(TestCase):
    """
    Test case for validating the `UpdateUserFormTest` in different scenarios.
    """
    def test_update_user_form_valid(self):
        """
        Test that the UpdateUserForm is valid when all fields are filled with valid data.
        """
        form_data = {
            'username': 'Viki',  # valid username
            'first_name': 'Victoria', # valid first name
            'last_name': 'Kitanova', # valid last name
            'email': 'victoria@gmail.com' # valid email
        }
        form = UpdateUserForm(data=form_data)
        self.assertTrue(form.is_valid())  # The form should be valid with the provided data

    def test_update_user_form_invalid_email(self):
        """
        Test that the UpdateUserForm is invalid when an invalid email is provided.
        """
        form_data = {
            'username': 'Viki',
            'first_name': 'Victoria',
            'last_name': 'Kitanova',
            'email': 'invalid-email'  # invalid email
        }
        form = UpdateUserForm(data=form_data)
        self.assertFalse(form.is_valid())  # The form should be invalid due to the email

class ProfileModelTest(TestCase):
    """
    Test case for validating the ProfileModelTest in different scenarios.
    """
    def setUp(self):
        # Creating a user before each test to ensure a clean state
        self.user = User.objects.create_user(username='Kali', password='testpassword')

        # Make sure no profile exists for this user
        Profile.objects.filter(user=self.user).delete()

    def test_profile_creation(self):
        """
        Test that a profile is created for a user automatically and is related correctly.
        """
        # Ensure that no profile exists before creating one
        profile = Profile.objects.filter(user=self.user).first()

        # Create a new profile linked to the user
        profile = Profile.objects.create(user=self.user)
        profile.phone = '847393020'
        profile.address = 'Street Petko Kunchev'
        profile.city = 'Haskovo'
        profile.country = 'Bulgaria'

        # Check that the profile is created correctly
        self.assertEqual(profile.user.username, 'Kali')
        self.assertEqual(profile.phone, '847393020')
        self.assertEqual(profile.address, 'Street Petko Kunchev')
        self.assertEqual(profile.city, 'Haskovo')
        self.assertEqual(profile.country, 'Bulgaria')


    def test_profile_fields(self):
        """
        Test that the profile fields can store the correct values.
        """
        # Create a new profile linked to the user with specific data
        profile = Profile.objects.create(
            user=self.user,
            phone='1234567890',
            address='Street Petko Kunchev',
            city='Sofia',
            country='Bulgaria'
        )

        # Check if the fields are correctly saved
        self.assertEqual(profile.phone, '1234567890')
        self.assertEqual(profile.address, 'Street Petko Kunchev')
        self.assertEqual(profile.city, 'Sofia')
        self.assertEqual(profile.country, 'Bulgaria')

class CustomerModelTest(TestCase):
    """
    Test case for validating the CustomerModelTest in different scenarios.
    """
    def setUp(self):
        """
        Prepare the test data by creating a user and associating it with a Customer.
        """
        self.user = User.objects.create_user(username='Mihi', password='testpassword')
        self.customer = Customer.objects.create(
            user=self.user,
            phone='12345678',
            email='mihi@gmail.com',
            password='testpassword',
            old_cart='some_cart_data'
        )

    def test_customer_creation(self):
        """
        Test that a Customer instance is created correctly with all the fields.
        """
        self.assertEqual(self.customer.user.username, 'Mihi')
        self.assertEqual(self.customer.phone, '12345678')
        self.assertEqual(self.customer.email, 'mihi@gmail.com')
        self.assertEqual(self.customer.password, 'testpassword')
        self.assertEqual(self.customer.old_cart, 'some_cart_data')
        self.assertIsNotNone(self.customer.data_created)


class TagModelTest(TestCase):
    """
    Test case for validating the TagModelTest in different scenarios.
    """
    def setUp(self):
        """
        Prepare the test data by creating a Tag.
        """
        self.tag = Tag.objects.create(name='Fiction')

    def test_tag_creation(self):
        """
        Test that a Tag instance is created correctly with the name field.
        """
        self.assertEqual(self.tag.name, 'Fiction')


class BookModelTest(TestCase):
    """
    Test case for validating the BookModelTest in different scenarios.
    """
    def setUp(self):
        """
        Prepare the test data by creating a Book and associating a Tag with it.
        """
        self.tag = Tag.objects.create(name='Science Fiction')
        self.book = Book.objects.create(
            title='Dune',
            author='Frank Herbert',
            price=29.99,
            publication=datetime.date(1965, 8, 1),
            pages=412,
            cover='Hardcover',
            descreption='A science fiction masterpiece',
        )
        self.book.tags.add(self.tag)

    def test_book_creation(self):
        """
        Test that a Book instance is created correctly with all the fields.
        """
        self.assertEqual(self.book.title, 'Dune')
        self.assertEqual(self.book.author, 'Frank Herbert')
        self.assertEqual(self.book.price, 29.99)
        self.assertEqual(self.book.publication, datetime.date(1965, 8, 1))
        self.assertEqual(self.book.pages, 412)
        self.assertEqual(self.book.cover, 'Hardcover')
        self.assertEqual(self.book.descreption, 'A science fiction masterpiece')
        self.assertIsNotNone(self.book.data_created)
        self.assertEqual(self.book.tags.count(), 1)  # Ensure the tag is added correctly



class ProductReviewsModelTest(TestCase):
    """
    Test case for validating the ProductReviewsModelTest in different scenarios.
    """
    def setUp(self):
        """
        Prepare the test data by creating a book and a user to associate the review with
        """
        self.user = User.objects.create_user(username='Qni', password='testpassword')
        self.book = Book.objects.create(
            title='Dune',
            author='Frank Herbert',
            price=29.99,
            publication='1965-08-01',
            pages=412,
            cover='Hardcover',
            descreption='A science fiction masterpiece.'
        )

    def test_product_review_creation(self):
        """
        Test that a ProductReview instance is created correctly with all the fields
        """
        review = ProductReviews.objects.create(
            book=self.book,
            user=self.user,
            content='Great book! Highly recommend.',
            stars=5
        )

        self.assertEqual(review.book, self.book)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.content, 'Great book! Highly recommend.')
        self.assertEqual(review.stars, 5)
        self.assertIsNotNone(review.data_created)

    def test_unique_review_per_user_per_book(self):
        """
        Test that a user can only review a book once. 
        """
        # Create the first review for the book by the user
        ProductReviews.objects.create(
            book=self.book,
            user=self.user,
            content='Great book! Highly recommend.',
            stars=5
        )
        # Try to create another review for the same book by the same user,
        # should raise IntegrityError
        with self.assertRaises(IntegrityError):
            ProductReviews.objects.create(
                book=self.book,
                user=self.user,
                content='Another review for the same book.',
                stars=4
            )

class LoginUserTests(TestCase):
    """
    Test case for user login functionality in the application.

    This class contains tests that verify correct login behavior for users, 
    both valid and invalid. It checks for correct redirection, login success, 
    and cart functionality after login.
    """
    def setUp(self):
        """
        Set up the test environment by creating a test user and associated customer.
        """
        # Create a test user
        self.user = User.objects.create_user(username='Olga', password='password123')

        # Create a Customer object for the user
        self.customer = Customer.objects.create(user=self.user,
                                                phone='1234567890',
                                                email='olga@gmail.com')
        self.customer.old_cart = json.dumps({'1': 2, '2': 3})
        self.customer.save()

    def test_login_valid_user(self):
        """
        Test that a valid user can log in.
        """
        logged_in = self.client.login(username='Olga', password='password123')
        response = self.client.post(reverse('login'), {
        'username': 'Olga',
        'password': 'password123',
        })

        # Ensure the login was successful
        self.assertTrue(logged_in)

        # Ensure the response is a redirect (302) to the home page
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the home page
        self.assertRedirects(response, reverse('home'))

        # Check if the user is actually logged in by inspecting the session
        self.assertTrue('_auth_user_id' in self.client.session)


    def test_login_invalid_user(self):
        """
        Test that an invalid login attempt redirects back to the login page with an error message.
        """
        response = self.client.post(reverse('login'), {
            'username': 'Kali', # Wrong username
            'password': '123', # Wrong password
        })

        # Check that the response redirects to login page
        self.assertRedirects(response, reverse('login'))

        # Check for the error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "There was an error, please try again!")


    def test_login_user_cart_is_loaded(self):
        """
        Test that the user's cart is loaded correctly after a successful login.
        """
        # Log in the user
        response = self.client.post(reverse('login'), {
            'username': 'Olga',
            'password': 'password123',
        })

        # Check if the user is redirected to the home page after login
        self.assertRedirects(response, reverse('home'))

        self.client.session['session_key'] = {'1': 2, '2': 3}
        self.client.session.save()

        # Check if the cart items were added correctly in the Cart
        cart = Cart(self.client)
        self.assertEqual(cart.get_quants(), {'1': 2, '2': 3})
