from django.contrib import admin

# Register your models here.
from restaurantApp.models import MenuItem, Cart, Order, OrderItem,Category
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
