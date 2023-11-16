from django.contrib import admin
from .models import Category, Cart, MenuItem, Order, OrderItem, Booking, Menu


# Register your models here.


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'price',
                    'menu_item_description']
    search_fields = ['name', 'price']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'reservation_date',
                    'reservation_slot']
    search_fields = ['first_name', 'reservation_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title']
    list_editable = ['title']
    ordering = ['id']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'menuitem',
                    'quantity', 'unit_price', 'price']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price',
                    'featured', 'category']
    search_fields = ['category']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'delivery_crew', 'status', 'total', 'date']
    list_editable = ['status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menuitem',  'price']
