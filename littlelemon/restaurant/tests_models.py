from django.test import TestCase, RequestFactory
from datetime import date
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from .models import Booking, Menu, Category, MenuItem, Cart, Order, OrderItem


# Create your tests here.


class BookingModelTest(TestCase):
    def setUp(self):
        Booking.objects.create(
            first_name='John',
            reservation_date=date(2023, 1, 1),
            reservation_slot=10
        )

    def test_booking_str_method(self):
        """
        Test the __str__ method of the Booking model.
        """
        booking = Booking.objects.get(first_name='John')
        self.assertEqual(str(booking), 'John')

    def test_booking_creation(self):
        """
        Test if a Booking instance can be created and saved to the database.
        """
        booking = Booking.objects.get(first_name='John')
        self.assertEqual(booking.reservation_date, date(2023, 1, 1))
        self.assertEqual(booking.reservation_slot, 10)


class MenuModelTest(TestCase):
    def setUp(self):
        Menu.objects.create(
            name='Burger',
            price=Decimal('9.99'),
            menu_item_description='A delicious burger with all the fixings.'
        )

    def test_menu_str_method(self):
        """
        Test the __str__ method of the Menu model.
        """
        menu_item = Menu.objects.get(name='Burger')
        self.assertEqual(str(menu_item), 'Burger')

    def test_menu_creation(self):
        """
        Test if a Menu instance can be created and saved to the database.
        """
        menu_item = Menu.objects.get(name='Burger')
        self.assertEqual(menu_item.price, Decimal('9.99'))
        self.assertEqual(menu_item.menu_item_description,
                         'A delicious burger with all the fixings.')


class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(
            slug='food',
            title='Food Category'
        )

    def test_category_str_method(self):
        """
        Test the __str__ method of the Category model.
        """
        category = Category.objects.get(slug='food')
        self.assertEqual(str(category), 'Food Category')

    def test_category_creation(self):
        """
        Test if a Category instance can be created and saved to the database.
        """
        category = Category.objects.get(slug='food')
        self.assertEqual(category.title, 'Food Category')


class MenuItemModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            slug='food',
            title='Food Category'
        )
        MenuItem.objects.create(
            title='Cheeseburger',
            price=Decimal('8.99'),
            featured=True,
            category=category
        )

    def test_menu_item_str_method(self):
        """
        Test the __str__ method of the MenuItem model.
        """
        menu_item = MenuItem.objects.get(title='Cheeseburger')
        self.assertEqual(str(menu_item), 'Cheeseburger')

    def test_menu_item_creation(self):
        """
        Test if a MenuItem instance can be created and saved to the database.
        """
        menu_item = MenuItem.objects.get(title='Cheeseburger')
        self.assertEqual(menu_item.price, Decimal('8.99'))
        self.assertTrue(menu_item.featured)
        self.assertEqual(menu_item.category.title, 'Food Category')


class CartModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        category = Category.objects.create(
            slug='food',
            title='Food Category'
        )
        menu_item = MenuItem.objects.create(
            title='Cheeseburger',
            price=Decimal('8.99'),
            featured=True,
            category=category
        )
        Cart.objects.create(
            user=user,
            menuitem=menu_item,
            quantity=2,
            unit_price=Decimal('8.99'),
            price=Decimal('17.98')
        )

    def test_cart_creation(self):
        """
        Test if a Cart instance can be created and saved to the database.
        """
        cart_item = Cart.objects.get(quantity=2)
        self.assertEqual(cart_item.user.username, 'testuser')
        self.assertEqual(cart_item.menuitem.title, 'Cheeseburger')
        self.assertEqual(cart_item.unit_price, Decimal('8.99'))
        self.assertEqual(cart_item.price, Decimal('17.98'))

    def test_cart_unique_together_constraint(self):
        """
        Test the unique_together constraint for menuitem and user.
        """
        user = User.objects.create_user(
            username='testuser2', password='testpassword')
        cart_item_duplicate = Cart(
            user=user,
            menuitem=MenuItem.objects.get(title='Cheeseburger'),
            quantity=1,
            unit_price=Decimal('8.99'),
            price=Decimal('8.99')
        )


class OrderModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        delivery_crew = User.objects.create_user(
            username='deliveryuser', password='deliverypassword')
        Order.objects.create(
            user=user,
            delivery_crew=delivery_crew,
            status=True,
            total=Decimal('25.99'),
            date='2023-01-15'
        )

    def test_order_creation(self):
        """
        Test if an Order instance can be created and saved to the database.
        """
        order = Order.objects.get(total=Decimal('25.99'))
        self.assertEqual(order.user.username, 'testuser')
        self.assertEqual(order.delivery_crew.username, 'deliveryuser')
        self.assertTrue(order.status)

    def test_order_delivery_crew_set_null(self):
        """
        Test if the delivery_crew field is set to NULL on deletion of the associated user.
        """
        delivery_crew_user = User.objects.get(username='deliveryuser')
        delivery_crew_user.delete()
        order = Order.objects.get(total=Decimal('25.99'))
        self.assertIsNone(order.delivery_crew)


class OrderItemModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        delivery_crew = User.objects.create_user(
            username='deliveryuser', password='deliverypassword')
        order = Order.objects.create(
            user=user,
            delivery_crew=delivery_crew,
            status=True,
            total=Decimal('25.99'),
            date='2023-01-15'
        )
        category = Category.objects.create(
            slug='food',
            title='Food Category'
        )
        menu_item = MenuItem.objects.create(
            title='Cheeseburger',
            price=Decimal('8.99'),
            featured=True,
            category=category
        )
        OrderItem.objects.create(
            order=order,
            menuitem=menu_item,
            quantity=2,
            price=Decimal('17.98')
        )

    def test_order_item_creation(self):
        """
        Test if an OrderItem instance can be created and saved to the database.
        """
        order_item = OrderItem.objects.get(quantity=2)
        self.assertEqual(order_item.order.total, Decimal('25.99'))
        self.assertEqual(order_item.menuitem.title, 'Cheeseburger')
        self.assertEqual(order_item.price, Decimal('17.98'))
