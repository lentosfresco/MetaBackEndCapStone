from django.test import TestCase, RequestFactory
from datetime import date
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from .views import reservations, book


# Create your tests here.


class ReservationsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_reservations_view(self):
        """
        Test the reservations view.
        """
        request = self.factory.get('/reservations/')
        request.user = self.user
        response = reservations(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bookings')

    def test_reservations_view_with_date_param(self):
        """
        Test the reservations view with a date parameter.
        """
        date_param = '2023-01-15'
        request = self.factory.get(f'/reservations/?date={date_param}')
        request.user = self.user
        response = reservations(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bookings')


class BookViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_book_view_get_request(self):
        """
        Test the book view with a GET request.
        """
        request = self.factory.get('/book/')
        request.user = self.user
        response = book(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_book_view_post_request_valid_form(self):
        """
        Test the book view with a POST request and a valid form.
        """
        data = {
            'first_name': 'John',
            'reservation_date': '2023-01-15',
            'reservation_slot': 10
        }
        request = self.factory.post('/book/', data)
        request.user = self.user
        response = book(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    def test_book_view_post_request_invalid_form(self):
        """
        Test the book view with a POST request and an invalid form.
        """
        data = {}  # Invalid data, missing required fields
        request = self.factory.post('/book/', data)
        request.user = self.user
        response = book(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
